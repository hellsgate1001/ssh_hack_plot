import argparse


def plot_ssh(args):
    import pdb;pdb.set_trace()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ssh_log', help='Absolute path to the system SSH log')
    args = parser.parse_args()

    plot_ssh(args)
