# -*- coding: utf-8 -*-
"""
CLI entry point.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from riocloud_reader import Reader
from riocloud_reader.schema import UnifiedInbox


def main():
    parser = argparse.ArgumentParser(
        description="Riocloud Reader - Universal content reader"
    )
    parser.add_argument("urls", nargs="+", help="URL(s) to fetch")
    parser.add_argument("-o", "--output", help="Output directory for Markdown files")
    parser.add_argument("-i", "--inbox", help="Inbox JSON file path")
    parser.add_argument("--list", action="store_true", help="List inbox contents")
    
    args = parser.parse_args()
    
    # Handle inbox
    inbox = None
    if args.inbox or args.list:
        inbox_path = args.inbox or "inbox.json"
        inbox = UnifiedInbox(inbox_path)
        
        if args.list:
            print(f"Inbox: {inbox_path}")
            print(f"Total items: {len(inbox.items)}\n")
            for item in inbox.items:
                print(f"- [{item.source_type.value}] {item.title[:60]}")
                print(f"  {item.url[:50]}...")
            return
    
    # Initialize reader
    reader = Reader(inbox=inbox)
    
    async def fetch():
        results = await reader.read_batch(args.urls)
        
        for content in results:
            print(f"\n{'='*60}")
            print(f"Title: {content.title}")
            print(f"Source: {content.source_type.value}")
            print(f"URL: {content.url}")
            print(f"{'='*60}\n")
            print(content.content[:1000])
            if len(content.content) > 1000:
                print(f"\n... ({len(content.content) - 1000} more characters)")
            
            # Save to file if requested
            if args.output:
                output_dir = Path(args.output)
                output_dir.mkdir(parents=True, exist_ok=True)
                
                filename = f"{content.id}_{content.source_type.value}.md"
                filepath = output_dir / filename
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content.to_markdown())
                print(f"\nSaved to: {filepath}")
    
    asyncio.run(fetch())


if __name__ == "__main__":
    main()
