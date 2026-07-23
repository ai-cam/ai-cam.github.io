#!/usr/bin/env python3
"""
Test Suite for Branch Protection Functionality

This test suite validates all aspects of branch protection functionality
and security controls to ensure they work as expected.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import importlib.util

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
sys.path.insert(0, scripts_dir)

# Import module with hyphenated name using importlib
spec = importlib.util.spec_from_file_location(
    "configure_branch_protection",
    os.path.join(scripts_dir, "configure-branch-protection.py")
)
configure_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(configure_module)

BranchProtectionConfigurator = configure_module.BranchProtectionConfigurator
get_default_protection_settings = configure_module.get_default_protection_settings
validate_protection_settings = configure_module.validate_protection_settings


class TestBranchProtectionSettings(unittest.TestCase):
    """Test branch protection settings and validation."""
    
    def test_default_protection_settings(self):
        """Test that default protection settings are properly structured."""
        settings = get_default_protection_settings()
        
        self.assertIn('required_pull_request_reviews', settings)
        self.assertIn('required_status_checks', settings)
        self.assertEqual(settings['enforce_admins'], True)
        self.assertEqual(settings['allow_force_pushes'], False)
        self.assertEqual(settings['allow_deletions'], False)
        self.assertEqual(settings['required_conversation_resolution'], True)
    
    def test_default_pr_review_settings(self):
        """Test PR review requirements in default settings."""
        settings = get_default_protection_settings()
        pr_settings = settings['required_pull_request_reviews']
        
        self.assertEqual(pr_settings['required_approving_review_count'], 1)
        self.assertEqual(pr_settings['dismiss_stale_reviews'], True)
        self.assertEqual(pr_settings['require_code_owner_reviews'], False)
    
    def test_default_status_check_settings(self):
        """Test status check requirements in default settings."""
        settings = get_default_protection_settings()
        status_settings = settings['required_status_checks']
        
        self.assertEqual(status_settings['strict'], True)
        self.assertIn('ci/build', status_settings['contexts'])
        self.assertIn('ci/test', status_settings['contexts'])
        self.assertIn('ci/lint', status_settings['contexts'])


class TestProtectionValidation(unittest.TestCase):
    """Test branch protection validation logic."""
    
    def test_validation_compliant_branch(self):
        """Test validation when branch is already compliant."""
        desired = get_default_protection_settings()
        current = {
            'protected': True,
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
            'allow_force_pushes': False,
            'allow_deletions': False,
            'required_conversation_resolution': True,
        }
        
        result = validate_protection_settings(desired, current)
        self.assertTrue(result['is_compliant'])
        self.assertEqual(len(result['differences']), 0)
    
    def test_validation_unprotected_branch(self):
        """Test validation when branch is not protected."""
        desired = get_default_protection_settings()
        current = None
        
        result = validate_protection_settings(desired, current)
        self.assertFalse(result['is_compliant'])
        self.assertTrue(result['missing_protection'])
        self.assertIn("Branch is not currently protected", result['differences'])
    
    def test_validation_pr_review_mismatch(self):
        """Test validation detects PR review count mismatch."""
        desired = get_default_protection_settings()
        desired['required_pull_request_reviews']['required_approving_review_count'] = 2
        
        current = {
            'protected': True,
            'required_pull_request_reviews': {
                'required_approving_review_count': 1,
                'dismiss_stale_reviews': True,
                'require_code_owner_reviews': False,
            },
            'required_status_checks': {
                'strict': True,
                'contexts': ['ci/build', 'ci/test'],
            },
            'enforce_admins': True,
            'allow_force_pushes': False,
            'allow_deletions': False,
        }
        
        result = validate_protection_settings(desired, current)
        self.assertFalse(result['is_compliant'])
        self.assertTrue(any('PR review count mismatch' in diff for diff in result['differences']))
    
    def test_validation_status_check_mismatch(self):
        """Test validation detects status check context mismatch."""
        desired = get_default_protection_settings()
        current = {
            'protected': True,
            'required_pull_request_reviews': {
                'required_approving_review_count': 1,
                'dismiss_stale_reviews': True,
            },
            'required_status_checks': {
                'strict': True,
                'contexts': ['ci/build'],  # Missing ci/test and ci/lint
            },
            'enforce_admins': True,
            'allow_force_pushes': False,
            'allow_deletions': False,
        }
        
        result = validate_protection_settings(desired, current)
        self.assertFalse(result['is_compliant'])
        self.assertTrue(any('Status check contexts mismatch' in diff for diff in result['differences']))
    
    def test_validation_force_push_allowed(self):
        """Test validation detects when force pushes are incorrectly allowed."""
        desired = get_default_protection_settings()
        current = {
            'protected': True,
            'required_pull_request_reviews': {
                'required_approving_review_count': 1,
                'dismiss_stale_reviews': True,
            },
            'required_status_checks': {
                'strict': True,
                'contexts': ['ci/build', 'ci/test', 'ci/lint'],
            },
            'enforce_admins': True,
            'allow_force_pushes': True,  # Should be False
            'allow_deletions': False,
        }
        
        result = validate_protection_settings(desired, current)
        self.assertFalse(result['is_compliant'])
        self.assertTrue(any('allow_force_pushes' in diff for diff in result['differences']))
    
    def test_validation_enforce_admins_disabled(self):
        """Test validation detects when admin enforcement is disabled."""
        desired = get_default_protection_settings()
        current = {
            'protected': True,
            'required_pull_request_reviews': {
                'required_approving_review_count': 1,
                'dismiss_stale_reviews': True,
            },
            'required_status_checks': {
                'strict': True,
                'contexts': ['ci/build', 'ci/test', 'ci/lint'],
            },
            'enforce_admins': False,  # Should be True
            'allow_force_pushes': False,
            'allow_deletions': False,
        }
        
        result = validate_protection_settings(desired, current)
        self.assertFalse(result['is_compliant'])
        self.assertTrue(any('enforce_admins' in diff for diff in result['differences']))


class TestBranchProtectionConfigurator(unittest.TestCase):
    """Test BranchProtectionConfigurator class."""
    
    @patch('github.Github')
    def test_initialization(self, mock_github_class):
        """Test configurator initialization."""
        mock_github = Mock()
        mock_repo = Mock()
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github
        
        configurator = BranchProtectionConfigurator(
            token='test_token',
            repo_name='test/repo',
            dry_run=True
        )
        
        self.assertEqual(configurator.repo_name, 'test/repo')
        self.assertTrue(configurator.dry_run)
        mock_github.get_repo.assert_called_once_with('test/repo')
    
    @patch('github.Github')
    def test_get_current_protection_unprotected(self, mock_github_class):
        """Test getting protection for unprotected branch."""
        mock_github = Mock()
        mock_repo = Mock()
        mock_branch = Mock()
        mock_branch.protected = False
        mock_repo.get_branch.return_value = mock_branch
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github
        
        configurator = BranchProtectionConfigurator(
            token='test_token',
            repo_name='test/repo',
            dry_run=True
        )
        
        result = configurator.get_current_protection('main')
        self.assertIsNone(result)
    
    @patch('github.Github')
    def test_get_current_protection_protected(self, mock_github_class):
        """Test getting protection for protected branch."""
        mock_github = Mock()
        mock_repo = Mock()
        mock_branch = Mock()
        mock_branch.protected = True
        
        # Mock protection object
        mock_protection = Mock()
        mock_pr_reviews = Mock()
        mock_pr_reviews.required_approving_review_count = 1
        mock_pr_reviews.dismiss_stale_reviews = True
        mock_pr_reviews.require_code_owner_reviews = False
        mock_pr_reviews.require_last_push_approval = False
        
        mock_status_checks = Mock()
        mock_status_checks.strict = True
        mock_status_checks.contexts = [Mock(context='ci/build')]
        
        mock_protection.required_pull_request_reviews = mock_pr_reviews
        mock_protection.required_status_checks = mock_status_checks
        mock_protection.enforce_admins = Mock(enabled=True)
        mock_protection.required_linear_history = Mock(enabled=False)
        mock_protection.allow_force_pushes = Mock(enabled=False)
        mock_protection.allow_deletions = Mock(enabled=False)
        mock_protection.required_conversation_resolution = Mock(enabled=True)
        mock_protection.lock_branch = Mock(enabled=False)
        
        mock_branch.get_protection.return_value = mock_protection
        mock_repo.get_branch.return_value = mock_branch
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github
        
        configurator = BranchProtectionConfigurator(
            token='test_token',
            repo_name='test/repo',
            dry_run=True
        )
        
        result = configurator.get_current_protection('main')
        self.assertIsNotNone(result)
        self.assertTrue(result['protected'])
        self.assertEqual(result['required_pull_request_reviews']['required_approving_review_count'], 1)


class TestDirectPushPrevention(unittest.TestCase):
    """Test that direct pushes are prevented."""
    
    def test_force_push_disabled(self):
        """Test that force pushes are disabled in default settings."""
        settings = get_default_protection_settings()
        self.assertFalse(settings['allow_force_pushes'])
    
    def test_deletions_disabled(self):
        """Test that branch deletions are disabled in default settings."""
        settings = get_default_protection_settings()
        self.assertFalse(settings['allow_deletions'])
    
    def test_enforce_admins_enabled(self):
        """Test that admin enforcement is enabled."""
        settings = get_default_protection_settings()
        self.assertTrue(settings['enforce_admins'])


class TestPullRequestRequirements(unittest.TestCase):
    """Test pull request review requirements."""
    
    def test_pr_reviews_required(self):
        """Test that PR reviews are required."""
        settings = get_default_protection_settings()
        self.assertIn('required_pull_request_reviews', settings)
        pr_settings = settings['required_pull_request_reviews']
        self.assertGreater(pr_settings['required_approving_review_count'], 0)
    
    def test_stale_reviews_dismissed(self):
        """Test that stale reviews are dismissed."""
        settings = get_default_protection_settings()
        pr_settings = settings['required_pull_request_reviews']
        self.assertTrue(pr_settings['dismiss_stale_reviews'])


class TestStatusCheckRequirements(unittest.TestCase):
    """Test status check requirements."""
    
    def test_status_checks_required(self):
        """Test that status checks are required."""
        settings = get_default_protection_settings()
        self.assertIn('required_status_checks', settings)
        status_settings = settings['required_status_checks']
        self.assertGreater(len(status_settings['contexts']), 0)
    
    def test_strict_status_checks(self):
        """Test that strict status checks are enabled."""
        settings = get_default_protection_settings()
        status_settings = settings['required_status_checks']
        self.assertTrue(status_settings['strict'])


if __name__ == '__main__':
    unittest.main()

