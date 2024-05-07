def add_generic_cli(parser):
    parser.add_argument("--use_local_roborio", action="store_true")
    parser.add_argument("--use_local_bazelrio", action="store_true")
    parser.add_argument("--use_local_rules_pmd", action="store_true")
    parser.add_argument("--use_local_rules_checkstyle", action="store_true")
    parser.add_argument("--use_local_rules_wpiformat", action="store_true")
    parser.add_argument("--use_local_rules_spotless", action="store_true")
    parser.add_argument("--use_local_rules_wpi_styleguide", action="store_true")
    parser.add_argument("--use_local_rules_bzlmodrio_jdk", action="store_true")
    parser.add_argument("--force_tests", action="store_true")


class GenericCliArgs:
    def __init__(self, args):
        self.use_local_roborio = args.use_local_roborio
        self.use_local_bazelrio = args.use_local_bazelrio

        self.use_local_rules_pmd = args.use_local_rules_pmd
        self.use_local_rules_checkstyle = args.use_local_rules_checkstyle
        self.use_local_rules_wpiformat = args.use_local_rules_wpiformat
        self.use_local_rules_spotless = args.use_local_rules_spotless
        self.use_local_rules_wpi_styleguide = args.use_local_rules_wpi_styleguide
        self.use_local_rules_bzlmodrio_jdk = args.use_local_rules_bzlmodrio_jdk

        # self.use_local_rules_pmd = True
        # self.use_local_rules_checkstyle = True
        # self.use_local_rules_wpiformat = True
        # self.use_local_rules_spotless = True
        # self.use_local_rules_wpi_styleguide = True
