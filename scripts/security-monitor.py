#!/usr/bin/env python3
"""
GitHub Repository Security Monitoring Script

This script monitors repository events for security-relevant activities,
including protection rule changes, access modifications, and potential bypass attempts.
It provides comprehensive logging and alerting for repository security events.

Usage:
    python scripts/security-monitor.py [--repo REPO] [--event-type TYPE] [--event-data JSON]

Requirements:
    - GitHub Personal Access Token with 'repo' and 'admin:repo_hook' scopes
    - PyGithub library (install via: pip install PyGithub)
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
from github import Github
from github.GithubException import GithubException


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security-monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SecurityMonitor:
    """Monitors repository security events and generates alerts."""
    
    def __init__(self, token: str, repo_name: str):
        """
        Initialize the security monitor.
        
        Args:
            token: GitHub personal access token
            repo_name: Repository name in format 'owner/repo'
        """
        self.github = Github(token)
        self.repo_name = repo_name
        
        try:
            self.repo = self.github.get_repo(repo_name)
            logger.info(f"Successfully connected to repository: {repo_name}")
        except GithubException as e:
            logger.error(f"Failed to access repository {repo_name}: {e}")
            raise
    
    def check_branch_protection_status(self, branch: str = 'main') -> Dict[str, Any]:
        """
        Check current branch protection status.
        
        Args:
            branch: Branch name to check
            
        Returns:
            Dictionary with protection status information
        """
        try:
            branch_obj = self.repo.get_branch(branch)
            protection_status = {
                'branch': branch,
                'protected': branch_obj.protected,
                'timestamp': datetime.utcnow().isoformat(),
            }
            
            if branch_obj.protected:
                protection_obj = branch_obj.get_protection()
                
                # Extract protection details
                try:
                    pr_reviews = protection_obj.required_pull_request_reviews
                    if pr_reviews:
                        protection_status['pr_reviews'] = {
                            'required_count': pr_reviews.required_approving_review_count,
                            'dismiss_stale': pr_reviews.dismiss_stale_reviews,
                        }
                except Exception:
                    protection_status['pr_reviews'] = None
                
                try:
                    status_checks = protection_obj.required_status_checks
                    if status_checks:
                        protection_status['status_checks'] = {
                            'strict': status_checks.strict,
                            'contexts': [c.context for c in status_checks.contexts] if status_checks.contexts else [],
                        }
                except Exception:
                    protection_status['status_checks'] = None
                
                try:
                    protection_status['enforce_admins'] = protection_obj.enforce_admins.enabled if protection_obj.enforce_admins else False
                except Exception:
                    protection_status['enforce_admins'] = False
                
                try:
                    protection_status['allow_force_pushes'] = protection_obj.allow_force_pushes.enabled if protection_obj.allow_force_pushes else False
                except Exception:
                    protection_status['allow_force_pushes'] = False
                
                try:
                    protection_status['allow_deletions'] = protection_obj.allow_deletions.enabled if protection_obj.allow_deletions else False
                except Exception:
                    protection_status['allow_deletions'] = False
            
            return protection_status
            
        except GithubException as e:
            logger.error(f"Error checking branch protection: {e}")
            return {
                'branch': branch,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
            }
    
    def get_recent_commits(self, branch: str = 'main', limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent commits on a branch.
        
        Args:
            branch: Branch name
            limit: Maximum number of commits to retrieve
            
        Returns:
            List of commit information dictionaries
        """
        try:
            commits = self.repo.get_commits(sha=branch)[:limit]
            commit_list = []
            
            for commit in commits:
                commit_info = {
                    'sha': commit.sha,
                    'author': commit.author.login if commit.author else 'unknown',
                    'message': commit.commit.message[:100],  # First 100 chars
                    'date': commit.commit.author.date.isoformat() if commit.commit.author else None,
                    'url': commit.html_url,
                }
                commit_list.append(commit_info)
            
            return commit_list
            
        except GithubException as e:
            logger.error(f"Error retrieving commits: {e}")
            return []
    
    def get_recent_pull_requests(self, state: str = 'all', limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent pull requests.
        
        Args:
            state: PR state ('open', 'closed', 'all')
            limit: Maximum number of PRs to retrieve
            
        Returns:
            List of PR information dictionaries
        """
        try:
            prs = self.repo.get_pulls(state=state, sort='updated', direction='desc')[:limit]
            pr_list = []
            
            for pr in prs:
                pr_info = {
                    'number': pr.number,
                    'title': pr.title,
                    'state': pr.state,
                    'author': pr.user.login if pr.user else 'unknown',
                    'created_at': pr.created_at.isoformat() if pr.created_at else None,
                    'merged': pr.merged,
                    'mergeable': pr.mergeable,
                    'url': pr.html_url,
                }
                pr_list.append(pr_info)
            
            return pr_list
            
        except GithubException as e:
            logger.error(f"Error retrieving pull requests: {e}")
            return []
    
    def check_security_issues(self) -> List[Dict[str, Any]]:
        """
        Check for potential security issues.
        
        Returns:
            List of security issue dictionaries
        """
        issues = []
        
        # Check branch protection
        protection_status = self.check_branch_protection_status('main')
        
        if not protection_status.get('protected'):
            issues.append({
                'severity': 'high',
                'type': 'branch_protection',
                'message': 'Main branch is not protected',
                'timestamp': datetime.utcnow().isoformat(),
            })
        else:
            # Check for insecure settings
            if protection_status.get('allow_force_pushes'):
                issues.append({
                    'severity': 'high',
                    'type': 'force_push_allowed',
                    'message': 'Force pushes are allowed on protected branch',
                    'timestamp': datetime.utcnow().isoformat(),
                })
            
            if protection_status.get('allow_deletions'):
                issues.append({
                    'severity': 'high',
                    'type': 'deletions_allowed',
                    'message': 'Branch deletions are allowed',
                    'timestamp': datetime.utcnow().isoformat(),
                })
            
            if not protection_status.get('enforce_admins'):
                issues.append({
                    'severity': 'medium',
                    'type': 'admin_enforcement_disabled',
                    'message': 'Admin enforcement is disabled',
                    'timestamp': datetime.utcnow().isoformat(),
                })
            
            if not protection_status.get('pr_reviews'):
                issues.append({
                    'severity': 'medium',
                    'type': 'no_pr_reviews',
                    'message': 'No PR review requirements configured',
                    'timestamp': datetime.utcnow().isoformat(),
                })
        
        return issues
    
    def process_webhook_event(self, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a webhook event for security monitoring.
        
        Args:
            event_type: Type of webhook event
            event_data: Event payload data
            
        Returns:
            Dictionary with processed event information
        """
        processed_event = {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'security_relevant': False,
            'alerts': [],
        }
        
        # Check for security-relevant events
        security_event_types = [
            'push', 'pull_request', 'repository', 'branch_protection_rule',
            'member', 'membership', 'team', 'team_add'
        ]
        
        if event_type in security_event_types:
            processed_event['security_relevant'] = True
            
            # Process specific event types
            if event_type == 'push':
                # Check for direct push to main branch
                ref = event_data.get('ref', '')
                if ref == 'refs/heads/main' or ref.endswith('/main'):
                    processed_event['alerts'].append({
                        'severity': 'high',
                        'message': f'Direct push detected to main branch by {event_data.get("pusher", {}).get("name", "unknown")}',
                    })
                    logger.warning(f"SECURITY ALERT: Direct push to main branch detected")
            
            elif event_type == 'pull_request':
                action = event_data.get('action', '')
                pr_data = event_data.get('pull_request', {})
                
                if action == 'closed' and pr_data.get('merged'):
                    # Check if PR was merged without proper reviews
                    if pr_data.get('merged_by'):
                        processed_event['alerts'].append({
                            'severity': 'info',
                            'message': f'PR #{pr_data.get("number")} merged by {pr_data.get("merged_by", {}).get("login", "unknown")}',
                        })
            
            elif event_type == 'branch_protection_rule':
                action = event_data.get('action', '')
                if action in ['created', 'edited', 'deleted']:
                    processed_event['alerts'].append({
                        'severity': 'high',
                        'message': f'Branch protection rule {action}',
                    })
                    logger.warning(f"SECURITY ALERT: Branch protection rule {action}")
            
            elif event_type in ['member', 'membership', 'team', 'team_add']:
                processed_event['alerts'].append({
                    'severity': 'medium',
                    'message': f'Repository access change: {event_type}',
                })
                logger.info(f"Repository access change detected: {event_type}")
        
        return processed_event
    
    def generate_security_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive security report.
        
        Returns:
            Dictionary with security report data
        """
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'repository': self.repo_name,
            'branch_protection': self.check_branch_protection_status('main'),
            'security_issues': self.check_security_issues(),
            'recent_commits': self.get_recent_commits('main', limit=5),
            'recent_prs': self.get_recent_pull_requests(state='all', limit=5),
        }
        
        return report
    
    def log_security_event(self, event: Dict[str, Any], log_file: str = 'security-events.log'):
        """
        Log a security event to a file.
        
        Args:
            event: Event data dictionary
            log_file: Path to log file
        """
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Monitor GitHub repository security events'
    )
    parser.add_argument(
        '--token',
        default=os.environ.get('GITHUB_TOKEN'),
        help='GitHub personal access token (or set GITHUB_TOKEN env var)'
    )
    parser.add_argument(
        '--repo',
        default=os.environ.get('GITHUB_REPOSITORY', 'ai-cam/ai-cam.github.io'),
        help='Repository name in format owner/repo (or set GITHUB_REPOSITORY env var)'
    )
    parser.add_argument(
        '--event-type',
        help='Webhook event type to process'
    )
    parser.add_argument(
        '--event-data',
        help='Webhook event data as JSON string'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate and print security report'
    )
    
    args = parser.parse_args()
    
    if not args.token:
        logger.error("GitHub token is required. Set GITHUB_TOKEN env var or use --token")
        sys.exit(1)
    
    try:
        monitor = SecurityMonitor(token=args.token, repo_name=args.repo)
        
        if args.event_type and args.event_data:
            # Process webhook event
            try:
                event_data = json.loads(args.event_data)
            except json.JSONDecodeError:
                logger.error("Invalid JSON in event data")
                sys.exit(1)
            
            processed = monitor.process_webhook_event(args.event_type, event_data)
            monitor.log_security_event(processed)
            
            if processed['alerts']:
                for alert in processed['alerts']:
                    logger.warning(f"ALERT [{alert['severity']}]: {alert['message']}")
        
        if args.report:
            # Generate security report
            report = monitor.generate_security_report()
            print(json.dumps(report, indent=2))
            
            # Log security issues
            if report['security_issues']:
                logger.warning(f"Found {len(report['security_issues'])} security issues")
                for issue in report['security_issues']:
                    logger.warning(f"  [{issue['severity']}] {issue['message']}")
            else:
                logger.info("No security issues detected")
        
        # Always check for security issues if no specific action requested
        if not args.event_type and not args.report:
            issues = monitor.check_security_issues()
            if issues:
                logger.warning(f"Found {len(issues)} security issues")
                for issue in issues:
                    logger.warning(f"  [{issue['severity']}] {issue['message']}")
            else:
                logger.info("No security issues detected")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

