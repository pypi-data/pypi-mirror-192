import json
import time
import logging
import argparse
import geopandas as gpd

import gtfsutils
import gtfsutils.filter

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="GTFS Utilities")
    subparsers = parser.add_subparsers(dest="method", help="Method")

    # Filter method
    parser_filter = subparsers.add_parser("filter", help="Filter method")
    parser_filter.add_argument(dest="src", help="Input GTFS filepath")
    parser_filter.add_argument(dest="dst", help="Output GTFS filepath")
    parser_filter.add_argument(dest="bounds", help="Filter boundary")
    parser_filter.add_argument("-t", "--target",
        dest='target',
        help="Filter target (stops, shapes)",
        default="stops")
    parser_filter.add_argument("-o", "--operation",
        dest='operation',
        help="Filter operation (within, intersects)",
        default="within")
    parser_filter.add_argument("--overwrite", action='store_true',
        dest='overwrite', help="Overwrite if exists")
    parser_filter.add_argument('-v', '--verbose', action='store_true',
        dest='verbose', default=False,
        help="Verbose output")

    # Bounds method
    parser_bounds = subparsers.add_parser("bounds", help="Bounds method")
    parser_bounds.add_argument(dest="src", help="Input GTFS filepath")

    # Info method
    parser_info = subparsers.add_parser("info", help="Info method")
    parser_info.add_argument(dest="src", help="Input GTFS filepath")

    # Version method
    subparsers.add_parser("version", help="Print version")

    args = parser.parse_args()

    # # Verbose output
    if  'verbose' in args:
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=log_level)

    if args.method == "version":
        print(f"{gtfsutils.__name__} {gtfsutils.__version__}")

    elif args.method == "filter":
        assert args.bounds is not None, "No bounds defined"
        assert args.src is not None, "No input file specified"
        assert args.dst is not None, "No output file specified"

        # Prepare bounds
        if args.bounds.startswith("["):
            bounds = json.loads(args.bounds)
        else:
            bounds = gpd.read_file(args.bounds).geometry.unary_union

        # Load GTFS
        t = time.time()
        df_dict = gtfsutils.load_gtfs(args.src)
        duration = time.time() - t
        logger.debug(f"Loaded {args.src} in {duration:.2f}s")

        # Filter GTFS
        if args.target == 'stops':
            t = time.time()
            gtfsutils.filter.spatial_filter_by_stops(
                df_dict, bounds)
        elif args.target == 'shapes':
            t = time.time()
            gtfsutils.filter.spatial_filter_by_shapes(
                df_dict, bounds, operation=args.operation)
        else:
            raise ValueError(
                f"Target {args.target} not supported!")
        duration = time.time() - t
        logger.debug(f"Filtered {args.src} in {duration:.2f}s")

        # Save filtered GTFS
        t = time.time()
        gtfsutils.save_gtfs(df_dict, args.dst, ignore_required=True, overwrite=args.overwrite)
        duration = time.time() - t
        logger.debug(f"Saved to {args.dst} in {duration:.2f}s")
    
    elif args.method == "bounds":
        assert args.src is not None, "No input file specified"

        bounds = gtfsutils.get_bounding_box(args.src)
        print(bounds)
    
    elif args.method == "info":
        assert args.src is not None, "No input file specified"
        gtfsutils.print_info(args.src)

    elif args.method == "merge":
        raise NotImplementedError("Merge not implemented")


if __name__ == '__main__':
    main()
