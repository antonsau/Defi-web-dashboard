# Data source
SPREADSHEET_URL = ""
SHEET_NAME = '02 - Активные'

# All protocols are analyzed through 3 group of activities
GROUPS = ['protocols_nodes',
          'protocols_testing',
          'protocols_mainnet']

# All groups of activities have the same set of statuses (filter types and filter values)
FILTER_TYPES = {'waiting_for_updates': ['10'],
                'active': ['20', '21', '22', '23'],
                'waiting_for_rewards': ['80'],
                'in_queue': ['11'],
                'rewards_received': ['81'],
                'rewards_not_received': ['92', '93']}