import argparse


from App import App


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local",
        dest="local_flag",
        action="store_const",
        const=True,
        default=False,
        help="Use local config when running the application",
    )

    return parser.parse_args()


if __name__ == "__main__":
    print("Covirondelle-station started running...")

    arguments = parseArguments()
    App.run(local_flag=arguments.local_flag)
