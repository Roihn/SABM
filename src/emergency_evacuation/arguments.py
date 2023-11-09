import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("--seed", type=int, default=0)
argparser.add_argument('--need_obstacle', dest='need_obstacle', action='store_true')
argparser.set_defaults(need_obstacle=False)
argparser.add_argument("--num_humans", type=int, default=100)
argparser.add_argument('--fixed_agent', dest='random_agent', action='store_false')
argparser.set_defaults(random_agent=True)
argparser.add_argument('--not_panic', dest='is_panic', action='store_false')
argparser.set_defaults(is_panic=True)
argparser.add_argument("--task", type=int, default=1)
