import os
import shutil
import hashlib
import logging
import argparse
import time

def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    return logger

def ensure_directory_exists(path, logger):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory {path}")
        print(f"Created directory {path}")

def remove_extra_items(source_root, replica_path, logger):
    for item in os.listdir(replica_path):
        replica_item_path = os.path.join(replica_path, item)
        source_item_path = os.path.join(source_root, item)
        if not os.path.exists(source_item_path):
            if os.path.isfile(replica_item_path) or os.path.islink(replica_item_path):
                os.remove(replica_item_path)
                logger.info(f"Removed file {replica_item_path}")
                print(f"Removed file {replica_item_path}")
            elif os.path.isdir(replica_item_path):
                shutil.rmtree(replica_item_path)
                logger.info(f"Removed directory {replica_item_path}")
                print(f"Removed directory {replica_item_path}")

def sync_folders(source, replica, logger, use_hash=False):
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        replica_path = os.path.join(replica, relative_path)
        ensure_directory_exists(replica_path, logger)

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_path, file)
            if use_hash:
                if not os.path.exists(replica_file) or (os.path.getsize(source_file) != os.path.getsize(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file)):
                    shutil.copy2(source_file, replica_file)
                    print(f"Copied {source_file} to {replica_file}")
                    logger.info(f"Copied {source_file} to {replica_file}")
            else:
                if not os.path.exists(replica_file) or os.path.getmtime(source_file) != os.path.getmtime(replica_file):
                    shutil.copy2(source_file, replica_file)
                    print(f"Copied {source_file} to {replica_file}")
                    logger.info(f"Copied {source_file} to {replica_file}")
        
        remove_extra_items(root, replica_path, logger)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Synchronize two folders: source and replica.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument(
        "--log",
        default="sync_log.txt",
        help="Path to the log file (default: sync_log.txt)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Time interval (in seconds) between synchronizations (default: 30 seconds)"
    )
    parser.add_argument(
        "--use-hash",
        action="store_true",
        help="Enable MD5 hash comparison to detect changes in files"
    )
    args = parser.parse_args()
    logger = setup_logger(args.log)

    try:
        logger.info(f"Starting periodic synchronization every {args.interval} seconds.")
        print(f"Starting periodic synchronization every {args.interval} seconds. Press Ctrl+C to stop.")
        while True:
            start_time = time.time()
            sync_folders(args.source, args.replica, logger, args.use_hash)
            duration = time.time() - start_time
            logger.info(f"Synchronization completed in {duration:.2f} seconds.")
            print(f"Synchronization completed in {duration:.2f} seconds. Waiting for next interval...")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Synchronization stopped by user.")
        print("Synchronization stopped.")
    except Exception as e:
        logger.error(f"Error during synchronization: {e}")
        print(f"Error: {e}")
