

def add_generic_cli(parser):
    parser.add_argument('--use_local_roborio', action='store_true')
    parser.add_argument('--use_local_bazelrio', action='store_true')
    parser.add_argument('--use_local_rules_pmd', action='store_true')
    parser.add_argument('--use_local_rules_checkstyle', action='store_true')
    parser.add_argument('--use_local_rules_wpiformat', action='store_true')
    parser.add_argument('--force_tests', action='store_true')