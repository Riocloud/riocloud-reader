# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
CLI entry point.
"""

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path

from riocloud_reader import Reader
from riocloud_reader.schema import UnifiedInbox


def normalize_url(url: str) -> str:
    """Normalize URL: add https:// if missing scheme.
    
    Supports:
    - Full URLs: https://example.com -> https://example.com
    - Bare domains: example.com -> https://example.com
    """
    url = url.strip()
    
    # Already has scheme (http://, https://, ftp://, etc.)
    if "://" in url:
        return url
    
    # Bare domain: check if it looks like a domain
    # Must have at least one dot and no spaces
    if "." in url and " " not in url:
        return f"https://{url}"
    
    # Not a valid URL, return as-is (will fail later)
    return url


def save_to_obsidian(content, vault_path: str) -> str:
    """Save content to Obsidian vault.
    
    Creates date-based folder structure: vault/YYYY-MM/source_type/filename.md
    """
    from datetime import datetime
    
    vault = Path(vault_path)
    if not vault.exists():
        vault.mkdir(parents=True, exist_ok=True)
    
    # Date-based folder
    date_folder = datetime.now().strftime("%Y-%m")
    source_folder = content.source_type.value
    
    # Create folder structure
    target_dir = vault / date_folder / source_folder
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename from title
    safe_title = re.sub(r'[<>:"/\\|?*]', '', content.title)
    safe_title = safe_title[:50].strip()
    if not safe_title:
        safe_title = "untitled"
    
    # Add content ID to ensure uniqueness
    filename = f"{content.id[:8]}_{safe_title}.md"
    filepath = target_dir / filename
    
    # Write content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.to_markdown())
    
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(
        description="Riocloud Reader - Universal content reader"
    )
    parser.add_argument("urls", nargs="*", help="URL(s) to fetch")
    parser.add_argument("-o", "--output", help="Output directory for Markdown files")
    parser.add_argument("-i", "--inbox", help="Inbox JSON file path")
    parser.add_argument("--list", action="store_true", help="List inbox contents")
    parser.add_argument(
        "--obsidian",
        help="Obsidian vault path. If set, content is written to vault with date-based folders"
    )
    parser.add_argument(
        "--login",
        choices=["xhs", "twitter", "wechat"],
        help="Login to platform for authenticated access"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run login in headless mode (for --login)"
    )
    
    args = parser.parse_args()
    
    # Handle login command
    if args.login:
        if args.login == "xhs":
            from riocloud_reader.parsers.xhs import login_xhs
            asyncio.run(login_xhs(headless=args.headless))
        elif args.login == "twitter":
            from riocloud_reader.parsers.twitter import login_twitter
            asyncio.run(login_twitter(headless=args.headless))
        elif args.login == "wechat":
            print("WeChat login not yet implemented")
        return
    
    # Normalize URLs: add https:// for bare domains
    urls = [normalize_url(url) for url in args.urls]
    
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
        results = await reader.read_batch(urls)
        
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
            
            # Save to Obsidian vault if requested
            if args.obsidian:
                obsidian_path = save_to_obsidian(content, args.obsidian)
                print(f"\nSaved to Obsidian: {obsidian_path}")
    
    asyncio.run(fetch())


if __name__ == "__main__":
    main()
