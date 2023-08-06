import argparse
import cv2 as cv
from TwitterGraph.manager import GraphManager
from TwitterGraph.multigraph import MultiG

def cli():
    parser = argparse.ArgumentParser(description='Twitter-Graph')
    parser.add_argument('--victims', type=str, help='String de nombre o nombres de víctimas')
    parser.add_argument('--n_tweets', type=int, help='Número de tweets a scrappear')
    parser.add_argument('--depth', type=int, help='Profundidad del scrapeo')

    args = parser.parse_args()
    
    if not '-' in args.victims:
        manager = GraphManager(args.victims, args.n_tweets, args.depth)
        img = cv.imread(manager.dir+manager.path[:-4]+'.png')
    else: 
        manager = MultiG(args.victims.split('-'), args.n_tweets)
        img = cv.imread(manager.path[:-4]+'.png')
    
    if img is None:
        exit(1)

    cv.imshow("Display window", img)
    cv.waitKey(0)