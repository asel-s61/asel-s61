"""Render public GitHub profile telemetry without third-party image services."""
import datetime
import html
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUERY = '''query {
  user(login: "asel-s61") {
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100, orderBy: {field: UPDATED_AT, direction: DESC}) {
      totalCount nodes {stargazerCount languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {edges {size node {name color}}}}
    }
    contributionsCollection {
      totalCommitContributions totalPullRequestContributions totalIssueContributions
      contributionCalendar {totalContributions weeks {contributionDays {date contributionCount}}}
    }
  }
}'''
result = json.loads(subprocess.check_output(['gh', 'api', 'graphql', '-f', 'query=' + QUERY], text=True))
if result.get('errors'):
    raise RuntimeError(result['errors'])
user = result['data']['user']
repos = user['repositories']
contributions = user['contributionsCollection']
calendar = contributions['contributionCalendar']
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="620" viewBox="0 0 1440 620" role="img" aria-labelledby="title desc">
<title id="title">Asel / GitHub telemetry</title><desc id="desc">Public GitHub contributions over the last year, repositories, stars, language breakdown and contribution heatmap. Updated daily.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#142139"/><stop offset="1" stop-color="#0b111e"/></linearGradient></defs>
<style>@keyframes rise{from{transform:scaleX(0)}to{transform:scaleX(1)}}@keyframes pulse{50%{opacity:.35}}.bar{animation:rise 1.6s ease-out;transform-box:fill-box;transform-origin:left}.live{animation:pulse 3s infinite}@media(prefers-reduced-motion:reduce){.bar,.live{animation:none}}</style>
<rect x="1" y="1" width="1438" height="618" rx="20" fill="url(#bg)" stroke="#35415a"/>
<circle class="live" cx="39" cy="43" r="5" fill="#cc87a0"/>
<text x="58" y="49" fill="#eee5eb" font-family="Consolas,monospace" font-size="18" font-weight="700">GITHUB TELEMETRY / 061</text>''']

def text(x, y, content, size=14, color='#9caac1', extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Consolas,monospace" font-size="{size}" {extra}>{html.escape(str(content))}</text>'

parts.append(text(1401, 48, stamp, 12, extra='text-anchor="end"'))
metrics = [('CONTRIBUTIONS / YEAR', calendar['totalContributions']),
           ('COMMITS / YEAR', contributions['totalCommitContributions']),
           ('PULL REQUESTS / YEAR', contributions['totalPullRequestContributions']),
           ('PUBLIC REPOSITORIES', repos['totalCount']),
           ('STARS / TOP 100 REPOS', sum(r['stargazerCount'] for r in repos['nodes']))]
for i, (label, value) in enumerate(metrics):
    x = 28 + i * 279
    parts.append(f'<rect x="{x}" y="82" width="264" height="120" rx="12" fill="#101a2c" stroke="#303c53"/>')
    parts += [text(x + 19, 110, label, 11), text(x + 19, 170, value, 45, '#e7bdcf')]
    parts.append(f'<path class="bar" d="M{x+20} 185h224" stroke="#913b5b" stroke-width="3"/>')

parts.append(text(31, 246, '01 / LANGUAGE MIX', 13, '#d6bccb'))
languages = {}
for repo in repos['nodes']:
    for edge in repo['languages']['edges']:
        name = edge['node']['name']
        languages[name] = languages.get(name, 0) + edge['size']
top = sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5]
total = sum(languages.values())
palette = ['#b36385', '#718aaf', '#81486d', '#b8abc5', '#476783']
x = 32
for index, (name, size) in enumerate(top):
    width = 1376 * size / max(total, 1)
    parts.append(f'<rect class="bar" x="{x}" y="264" width="{width}" height="16" fill="{palette[index]}"/>')
    x += width
    parts.append(text(32 + index * 278, 309, f'{name} {size / max(total, 1):.1%}', 13, palette[index]))
parts.append(text(32, 337, 'Language bytes across up to 100 recently updated public repositories.', 11))
parts.append(text(31, 382, '02 / EVERY COMMIT LEAVES A TRACE', 13, '#d6bccb'))
colors = ['#1b2940', '#4c253d', '#743451', '#a24d6f', '#d18ca4']
for week_index, week in enumerate(calendar['weeks']):
    for day_index, day in enumerate(week['contributionDays']):
        weekday = (datetime.date.fromisoformat(day['date']).weekday() + 1) % 7
        count = day['contributionCount']
        level = 0 if count == 0 else min(4, 1 + (count >= 3) + (count >= 6) + (count >= 10))
        parts.append(f'<rect x="{32+week_index*25}" y="{404+weekday*22}" width="20" height="17" rx="3" fill="{colors[level]}"><title>{day["date"]}: {count} contributions</title></rect>')
parts.append(text(32, 587, 'PUBLIC ACTIVITY / LAST 12 MONTHS', 11))
parts.append(text(1400, 587, 'DATA: GITHUB API / UPDATED DAILY', 11, extra='text-anchor="end"'))
parts.append('</svg>')
(ROOT / 'assets' / 'telemetry.svg').write_text(''.join(parts), encoding='utf-8')
print('Updated telemetry.svg from GitHub API')
