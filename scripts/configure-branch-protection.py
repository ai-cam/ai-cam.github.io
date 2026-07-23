#!/usr/bin/env python3
"""
GitHub Branch Protection Configuration Script

This script programmatically configures GitHub branch protection rules via the GitHub API.
It validates and applies branch protection settings consistently, with error handling and logging.

Usage:
    python scripts/configure-branch-protection.py [--dry-run] [--token TOKEN] [--repo REPO] [--branch BRANCH]

Requirements:
    - GitHub Personal Access Token with 'repo' scope
    - PyGithub library (install via: pip install PyGithub)
"""

import argparse
import logging
import os
import sys
from typing import Dict, Any, Optional
from github import Github
from github.GithubException import GithubException


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('branch-protection.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def validate_protection_settings(desired: Dict[str, Any], current: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare desired and current protection settings.
    
    Args:
        desired: Desired protection settings
        current: Current protection settings (None if not protected)
        
    Returns:
        Dictionary with validation results and differences
    """
    result = {
        'is_compliant': True,
        'differences': [],
        'missing_protection': current is None
    }
    
    if current is None:
        result['is_compliant'] = False
        result['differences'].append("Branch is not currently protected")
        return result
    
    # Compare PR review requirements
    desired_pr = desired.get('required_pull_request_reviews', {})
    current_pr = current.get('required_pull_request_reviews')
    
    if desired_pr and current_pr:
        if desired_pr.get('required_approving_review_count') != current_pr.get('required_approving_review_count'):
            result['is_compliant'] = False
            result['differences'].append(
                f"PR review count mismatch: desired={desired_pr.get('required_approving_review_count')}, "
                f"current={current_pr.get('required_approving_review_count')}"
            )
    elif desired_pr and not current_pr:
        result['is_compliant'] = False
        result['differences'].append("PR review requirements not configured")
    
    # Compare status checks
    desired_status = desired.get('required_status_checks', {})
    current_status = current.get('required_status_checks')
    
    if desired_status and current_status:
        desired_contexts = set(desired_status.get('contexts', []))
        current_contexts = set(current_status.get('contexts', []))
        
        if desired_contexts != current_contexts:
            result['is_compliant'] = False
            result['differences'].append(
                f"Status check contexts mismatch: desired={desired_contexts}, current={current_contexts}"
            )
        
        if desired_status.get('strict') != current_status.get('strict'):
            result['is_compliant'] = False
            result['differences'].append(
                f"Status check strict mode mismatch: desired={desired_status.get('strict')}, "
                f"current={current_status.get('strict')}"
            )
    elif desired_status and not current_status:
        result['is_compliant'] = False
        result['differences'].append("Status check requirements not configured")
    
    # Compare other settings
    settings_to_check = [
        'enforce_admins', 'required_linear_history', 'allow_force_pushes',
        'allow_deletions', 'required_conversation_resolution', 'lock_branch'
    ]
    
    for setting in settings_to_check:
        desired_val = desired.get(setting, False)
        current_val = current.get(setting, False)
        if desired_val != current_val:
            result['is_compliant'] = False
            result['differences'].append(
                f"{setting}: desired={desired_val}, current={current_val}"
            )
    
    return result


class BranchProtectionConfigurator:
    """Manages GitHub branch protection configuration."""
    
    def __init__(self, token: str, repo_name: str, dry_run: bool = False):
        """
        Initialize the branch protection configurator.
        
        Args:
            token: GitHub personal access token
            repo_name: Repository name in format 'owner/repo'
            dry_run: If True, only validate without making changes
        """
        self.github = Github(token)
        self.repo_name = repo_name
        self.dry_run = dry_run
        
        try:
            self.repo = self.github.get_repo(repo_name)
            logger.info(f"Successfully connected to repository: {repo_name}")
        except GithubException as e:
            logger.error(f"Failed to access repository {repo_name}: {e}")
            raise
    
    def get_current_protection(self, branch: str) -> Optional[Dict[str, Any]]:
        """
        Get current branch protection settings.
        
        Args:
            branch: Branch name
            
        Returns:
            Dictionary of current protection settings or None if not protected
        """
        try:
            branch_obj = self.repo.get_branch(branch)
            protection = branch_obj.protected
            
            if not protection:
                return None
            
            # Get protection details
            protection_obj = branch_obj.get_protection()
            
            current_settings = {
                'protected': True,
                'required_pull_request_reviews': None,
                'required_status_checks': None,
                'enforce_admins': None,
                'required_linear_history': None,
                'allow_force_pushes': None,
                'allow_deletions': None,
                'required_conversation_resolution': None,
                'lock_branch': None,
            }
            
            # Extract PR review requirements
            try:
                pr_reviews = protection_obj.required_pull_request_reviews
                if pr_reviews:
                    current_settings['required_pull_request_reviews'] = {
                        'required_approving_review_count': pr_reviews.required_approving_review_count,
                        'dismiss_stale_reviews': pr_reviews.dismiss_stale_reviews,
                        'require_code_owner_reviews': pr_reviews.require_code_owner_reviews,
                        'require_last_push_approval': getattr(pr_reviews, 'require_last_push_approval', False),
                    }
            except Exception as e:
                logger.warning(f"Could not retrieve PR review requirements: {e}")
            
            # Extract status check requirements
            try:
                status_checks = protection_obj.required_status_checks
                if status_checks:
                    current_settings['required_status_checks'] = {
                        'strict': status_checks.strict,
                        'contexts': [check.context for check in status_checks.contexts] if status_checks.contexts else [],
                    }
            except Exception as e:
                logger.warning(f"Could not retrieve status check requirements: {e}")
            
            # Extract other protection settings
            try:
                current_settings['enforce_admins'] = protection_obj.enforce_admins.enabled if protection_obj.enforce_admins else False
            except Exception:
                current_settings['enforce_admins'] = False
            
            try:
                current_settings['required_linear_history'] = protection_obj.required_linear_history.enabled if protection_obj.required_linear_history else False
            except Exception:
                current_settings['required_linear_history'] = False
            
            try:
                current_settings['allow_force_pushes'] = protection_obj.allow_force_pushes.enabled if protection_obj.allow_force_pushes else False
            except Exception:
                current_settings['allow_force_pushes'] = False
            
            try:
                current_settings['allow_deletions'] = protection_obj.allow_deletions.enabled if protection_obj.allow_deletions else False
            except Exception:
                current_settings['allow_deletions'] = False
            
            try:
                current_settings['required_conversation_resolution'] = protection_obj.required_conversation_resolution.enabled if protection_obj.required_conversation_resolution else False
            except Exception:
                current_settings['required_conversation_resolution'] = False
            
            try:
                current_settings['lock_branch'] = protection_obj.lock_branch.enabled if protection_obj.lock_branch else False
            except Exception:
                current_settings['lock_branch'] = False
            
            return current_settings
            
        except GithubException as e:
            if e.status == 404:
                logger.error(f"Branch '{branch}' not found")
                return None
            logger.error(f"Error retrieving branch protection: {e}")
            raise
    
    def validate_protection_settings(self, desired: Dict[str, Any], current: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare desired and current protection settings.
        
        Args:
            desired: Desired protection settings
            current: Current protection settings (None if not protected)
            
        Returns:
            Dictionary with validation results and differences
        """
        return validate_protection_settings(desired, current)
    
    def apply_protection(self, branch: str, settings: Dict[str, Any]) -> bool:
        """
        Apply branch protection settings.
        
        Args:
            branch: Branch name
            settings: Protection settings dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            logger.info(f"[DRY RUN] Would apply protection settings to branch '{branch}'")
            logger.info(f"[DRY RUN] Settings: {settings}")
            return True
        
        try:
            branch_obj = self.repo.get_branch(branch)
            
            # Build protection parameters
            protection_params = {}
            
            # PR review requirements
            if 'required_pull_request_reviews' in settings:
                pr_settings = settings['required_pull_request_reviews']
                protection_params['required_pull_request_reviews'] = {
                    'required_approving_review_count': pr_settings.get('required_approving_review_count', 1),
                    'dismiss_stale_reviews': pr_settings.get('dismiss_stale_reviews', True),
                    'require_code_owner_reviews': pr_settings.get('require_code_owner_reviews', False),
                    'require_last_push_approval': pr_settings.get('require_last_push_approval', False),
                }
            
            # Status check requirements
            if 'required_status_checks' in settings:
                status_settings = settings['required_status_checks']
                protection_params['required_status_checks'] = {
                    'strict': status_settings.get('strict', True),
                    'contexts': status_settings.get('contexts', []),
                }
            
            # Other protection settings
            protection_params['enforce_admins'] = settings.get('enforce_admins', True)
            protection_params['required_linear_history'] = settings.get('required_linear_history', False)
            protection_params['allow_force_pushes'] = settings.get('allow_force_pushes', False)
            protection_params['allow_deletions'] = settings.get('allow_deletions', False)
            protection_params['required_conversation_resolution'] = settings.get('required_conversation_resolution', True)
            protection_params['lock_branch'] = settings.get('lock_branch', False)
            
            # Apply protection
            branch_obj.edit_protection(**protection_params)
            logger.info(f"Successfully applied protection settings to branch '{branch}'")
            return True
            
        except GithubException as e:
            logger.error(f"Failed to apply protection settings: {e}")
            return False
    
    def configure_branch(self, branch: str, settings: Dict[str, Any]) -> bool:
        """
        Configure branch protection with validation.
        
        Args:
            branch: Branch name
            settings: Desired protection settings
            
        Returns:
            True if configuration is successful or already compliant
        """
        logger.info(f"Configuring branch protection for '{branch}'")
        
        # Get current settings
        current = self.get_current_protection(branch)
        
        # Validate
        validation = self.validate_protection_settings(settings, current)
        
        if validation['is_compliant']:
            logger.info(f"Branch '{branch}' protection settings are already compliant")
            return True
        
        # Log differences
        logger.warning(f"Branch '{branch}' protection settings are not compliant:")
        for diff in validation['differences']:
            logger.warning(f"  - {diff}")
        
        # Apply protection
        return self.apply_protection(branch, settings)


def get_default_protection_settings() -> Dict[str, Any]:
    """Get default branch protection settings for main branch."""
    return {
        'required_pull_request_reviews': {
            'required_approving_review_count': 1,
            'dismiss_stale_reviews': True,
            'require_code_owner_reviews': False,
            'require_last_push_approval': False,
        },
        'required_status_checks': {
            'strict': True,
            'contexts': ['ci/build', 'ci/test', 'ci/lint'],
        },
        'enforce_admins': True,
        'required_linear_history': False,
        'allow_force_pushes': False,
        'allow_deletions': False,
        'required_conversation_resolution': True,
        'lock_branch': False,
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Configure GitHub branch protection rules'
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
        '--branch',
        default='main',
        help='Branch name to protect (default: main)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate settings without making changes'
    )
    
    args = parser.parse_args()
    
    if not args.token:
        logger.error("GitHub token is required. Set GITHUB_TOKEN env var or use --token")
        sys.exit(1)
    
    try:
        configurator = BranchProtectionConfigurator(
            token=args.token,
            repo_name=args.repo,
            dry_run=args.dry_run
        )
        
        settings = get_default_protection_settings()
        success = configurator.configure_branch(args.branch, settings)
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

