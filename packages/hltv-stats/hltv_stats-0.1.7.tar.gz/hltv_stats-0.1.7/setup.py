# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hltv_stats']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'cuid>=0.3,<0.4',
 'loguru>=0.6.0,<0.7.0',
 'pytest>=7.2.1,<8.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'hltv-stats',
    'version': '0.1.7',
    'description': 'Simple parser for HLTV.org team stats and matches (using requests and bs4)',
    'long_description': '<p>\n  <img alt="Version" src="https://img.shields.io/badge/version-0.1.7-blue.svg?cacheSeconds=2592000" />\n  <a href="#" target="_blank">\n    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />\n  </a>\n</p>\n\n> Hi, I analyze hltv.org as a part of my pet project.\n> This parser can help you build a prematch analytics dataset with data from [Team stats]( https://www.hltv.org/stats/teams) and [Analytics](https://www.hltv.org/betting/analytics) pages.\n\n\n\n## Install\n\n```sh\npip install hltv-stats\n```\n\n## Usage\n#### ```HLTVMatch``` provides public methods for [Analytics](https://www.hltv.org/betting/analytics), use ```filename``` parameter to save data to a file.\n```sh\nfrom hltv_stats import HLTVMatch\nmatch_url = "/matches/2361342/natus-vincere-vs-outsiders-iem-katowice-2023"\nmatch = HLTVMatch(match_url)\n```\n```sh\nmatch.parse_analytics_summary(filename=None)\n```\n\n```sh\nResponse:\n\n[{\'team\': \'natus-vincere\',\n  \'indicator\': \'plus\',\n  \'insight\': \'natus vincere has better form ranking\',\n  \'match_id\': \'2361342\'},\n    ...\n]\n```\n```sh\nmatch.parse_head_to_head()\n```\n\n```sh\nResponse:\n\n[{\'player_team\': \'natus-vincere\',\n  \'player_nickname\': \'s1mple\',\n  \'table_3_months\': \'1.13\',\n  \'table_event\': \'1.17\',\n  \'match_id\': \'2361342\'},\n    ...\n]\n```\n```sh\nmatch.parse_pick_ban_stats()\n```\n\n```sh\nResponse:\n\n[{\'analytics_map_name\': \'mirage\',\n  \'team\': \'natus-vincere\',\n  \'analytics_map_stats_pick_percentage\': \'39%\',\n  \'analytics_map_stats_ban_percentage\': \'0%\',\n  \'analytics_map_stats_win_percentage\': \'29%\',\n  \'analytics_map_stats_played\': \'7\',\n  \'analytics_map_stats_comment\': \'First pick\',\n  \'match_id\': \'2361342\'},\n    ...\n]\n```\n```match.parse_analytics_center()``` method combines all above methods and returns a tuple of lists.\n\n#### ```HLTVTeam``` provides public methods for parsing [Team stats page]( https://www.hltv.org/stats/teams), with filtering by time using ```time_filter``` parameter, use ```filename``` parameter to save data to a file.\n```sh\nfrom hltv_stats import HLTVTeam\nteam = HLTVTeam("/4608/natus-vincere")\n#You can use match_id to assign team\'s current state(statistic) to specific match\n#this will add match_id field to all json files\nteam.match_id = match.match_id\n```\n```sh\n#time_filter: 3 - last 3 months, 6 - last 6 months, 0 - all time, ...\nteam.parse_matches(time_filter=1) #returns list of played matches in json format\nteam.parse_players(time_filter=1) #returns list of team players\' statistics in json format\nteam.parse_maps(time_filter=1) #returns maps statistics in json format\nteam.parse_events(time_filter=1) #returns events statistics in json format\n\nteam.parse_all_stats(time_filter=1)\n```\n```.parse_all_stats(time_filter=1)``` method combines all above methods and returns a tuple of lists.\n\n#### ```parse_upcoming_matches()``` method parses all upcoming matches from [Match page](https://www.hltv.org/matches).\n```sh\n#Parse upcoming matches and save to json files\n#:param months: list of months to parse, i.e. [1,3] <=> [last month, last 3 months]\n#:param with_teams: bool, if True, parse teams\' statistic as well\n\nfrom hltv_stats import parse_upcoming_matches\nparse_upcoming_matches(months=[1], with_teams=True)\n```\n\n\n```\nResult folder tree contains json files with all match data, and team data if with_teams=True.\n.\n├── configs - contains 2 config files: which holds data about all parsed matches and teams and are used by is_parsed() method to check if match is already parsed and skips it.\n├── output\n│   ├── matches \n│   └── teams\n```\n#### Also check out example.ipynb or contact me.\n\n### 🤝 Contributing\n\nContributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/a3agalyan/hltv-stats/issues). \n\n### Show your support\n\nGive a ⭐️ if this project helped you!',
    'author': 'Armen A',
    'author_email': 'agalyan.armen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/a3agalyan/hltv-stats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
