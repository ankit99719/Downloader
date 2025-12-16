"""
Batch Manager for Instagram Reel Downloader
Handles automatic batch processing of links
"""
import os

BATCH_SIZE = 10  # Number of links to process per batch
ALL_LINKS_FILE = "all_links.txt"
CURRENT_LINKS_FILE = "links.txt"
BATCH_PROGRESS_FILE = "batch_progress.txt"
COUNTER_FILE = "counter.txt"

def get_current_batch_number():
    """Get the current batch number from batch_progress.txt"""
    if not os.path.exists(BATCH_PROGRESS_FILE):
        with open(BATCH_PROGRESS_FILE, 'w', encoding='utf-8') as f:
            f.write('1')
        return 1
    
    with open(BATCH_PROGRESS_FILE, 'r', encoding='utf-8') as f:
        try:
            return int(f.read().strip())
        except ValueError:
            return 1

def set_batch_number(batch_num):
    """Set the current batch number in batch_progress.txt"""
    with open(BATCH_PROGRESS_FILE, 'w', encoding='utf-8') as f:
        f.write(str(batch_num))

def get_all_links():
    """Read all links from all_links.txt"""
    if not os.path.exists(ALL_LINKS_FILE):
        print(f"[ERROR] {ALL_LINKS_FILE} not found!")
        return []
    
    with open(ALL_LINKS_FILE, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    
    return links

def get_batch_links(batch_number, batch_size=BATCH_SIZE):
    """Get links for the specified batch number"""
    all_links = get_all_links()
    start_idx = (batch_number - 1) * batch_size
    end_idx = start_idx + batch_size
    
    batch_links = all_links[start_idx:end_idx]
    
    print(f"[LOG] Total links available: {len(all_links)}")
    print(f"[LOG] Batch {batch_number}: Processing links {start_idx + 1} to {min(end_idx, len(all_links))}")
    print(f"[LOG] Links in this batch: {len(batch_links)}")
    
    return batch_links

def prepare_current_batch():
    """Prepare links.txt with the current batch of links"""
    current_batch = get_current_batch_number()
    batch_links = get_batch_links(current_batch)
    
    if not batch_links:
        print(f"[LOG] No more links to process. All batches complete!")
        return False
    
    # Write current batch to links.txt
    with open(CURRENT_LINKS_FILE, 'w', encoding='utf-8') as f:
        for link in batch_links:
            f.write(f"{link}\n")
    
    print(f"[LOG] Prepared batch {current_batch} with {len(batch_links)} links")
    return True

def advance_to_next_batch():
    """Move to the next batch"""
    current_batch = get_current_batch_number()
    next_batch = current_batch + 1
    
    # Check if there are more links to process
    all_links = get_all_links()
    start_idx = (next_batch - 1) * BATCH_SIZE
    
    if start_idx >= len(all_links):
        print(f"[LOG] All batches completed! Total links processed: {len(all_links)}")
        return False
    
    set_batch_number(next_batch)
    print(f"[LOG] Advanced to batch {next_batch}")
    return True

def get_batch_info():
    """Get information about current batch progress"""
    current_batch = get_current_batch_number()
    all_links = get_all_links()
    total_links = len(all_links)
    
    total_batches = (total_links + BATCH_SIZE - 1) // BATCH_SIZE  # Ceiling division
    links_processed = (current_batch - 1) * BATCH_SIZE
    links_remaining = total_links - links_processed
    
    info = {
        'current_batch': current_batch,
        'total_batches': total_batches,
        'total_links': total_links,
        'links_processed': links_processed,
        'links_remaining': links_remaining,
        'batch_size': BATCH_SIZE
    }
    
    return info

def print_batch_status():
    """Print current batch status"""
    info = get_batch_info()
    
    print("\n" + "="*60)
    print("BATCH PROCESSING STATUS")
    print("="*60)
    print(f"Current Batch: {info['current_batch']} of {info['total_batches']}")
    print(f"Total Links: {info['total_links']}")
    print(f"Links Processed: {info['links_processed']}")
    print(f"Links Remaining: {info['links_remaining']}")
    print(f"Batch Size: {info['batch_size']}")
    print(f"Progress: {(info['links_processed'] / info['total_links'] * 100):.1f}%")
    print("="*60 + "\n")

if __name__ == "__main__":
    # When run directly, prepare the current batch
    print_batch_status()
    
    if prepare_current_batch():
        print("[SUCCESS] Current batch prepared in links.txt")
    else:
        print("[INFO] No more batches to process")
