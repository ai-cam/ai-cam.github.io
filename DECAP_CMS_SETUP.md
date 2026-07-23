# Decap CMS Integration with Branch Protection

## Overview

This repository uses branch protection rules to secure the `main` branch. However, **Decap CMS (Netlify CMS) requires the ability to push directly to a branch**, which conflicts with branch protection.

## Current Configuration

- **Branch Protection**: `main` branch requires PR reviews and blocks direct pushes
- **Decap CMS**: Configured with `git-gateway` backend pointing to `main` branch
- **Conflict**: Branch protection will block CMS commits

## Solutions

### Option 1: Use Separate Branch for CMS (Recommended)

Configure Decap CMS to push to a `cms-edits` branch, then use automated workflows to create PRs.

**Steps:**

1. **Update `admin/config.yml`:**
   ```yaml
   backend:
     name: git-gateway
     branch: cms-edits  # Change from 'main' to 'cms-edits'
   ```

2. **The GitHub Action workflow** (`.github/workflows/decap-cms-integration.yml`) will:
   - Automatically create PRs from `cms-edits` to `main`
   - Allow manual review and merge of CMS content
   - Maintain security while enabling CMS workflow

3. **Benefits:**
   - ✅ Maintains branch protection on `main`
   - ✅ CMS edits go through PR review process
   - ✅ Full audit trail of CMS changes
   - ✅ Can add automated checks before merging

### Option 2: GitHub App with Bypass Permissions

Configure a GitHub App with bypass permissions for CMS operations.

**Steps:**

1. Create a GitHub App with repository write permissions
2. Configure Decap CMS to use the GitHub App token
3. Add the GitHub App to branch protection bypass list
4. **Note**: This reduces security as it allows direct pushes

### Option 3: Modify Branch Protection (Not Recommended)

Allow specific users/apps to bypass branch protection.

**Security Risk**: This defeats the purpose of branch protection and is not recommended.

## Recommended Setup: Option 1

### Implementation Steps

1. **Update Decap CMS configuration:**
   ```yaml
   # admin/config.yml
   backend:
     name: git-gateway
     branch: cms-edits  # Changed from 'main'
   ```

2. **The workflow is already configured** in `.github/workflows/decap-cms-integration.yml`

3. **CMS Workflow:**
   - User edits content in Decap CMS
   - CMS commits to `cms-edits` branch
   - GitHub Action creates PR to `main`
   - PR requires review (can be automated for trusted users)
   - After approval, PR merges to `main`

### Customizing Auto-merge

To enable automatic merging of CMS edits (less secure but faster):

1. Edit `.github/workflows/decap-cms-integration.yml`
2. Uncomment the `direct-merge-cms` job
3. Configure appropriate security checks
4. **Warning**: This bypasses PR review - use with caution

### Status Checks

If you want CMS PRs to skip status checks:

1. Update branch protection settings
2. Configure status check bypass for CMS PRs
3. Or make status checks optional for CMS-related changes

## Testing

1. Make a test edit in Decap CMS
2. Verify commit goes to `cms-edits` branch
3. Check that PR is automatically created
4. Review and merge the PR
5. Verify changes appear on `main`

## Troubleshooting

### CMS commits are blocked

- **Issue**: Decap CMS cannot push to protected branch
- **Solution**: Ensure CMS is configured to use `cms-edits` branch, not `main`

### PRs not being created

- **Issue**: Workflow not triggering
- **Solution**: Check workflow file syntax and GitHub Actions permissions

### Status checks blocking merge

- **Issue**: Required status checks fail for CMS PRs
- **Solution**: Configure status check bypass or make checks optional for CMS branch

## Security Considerations

- **CMS edits should still be reviewed** before merging to `main`
- **Audit trail**: All CMS changes go through PRs, providing full history
- **Access control**: Limit who can use Decap CMS through Netlify Identity
- **Content validation**: Consider adding automated content checks in the workflow

## Questions?

For issues or questions about the CMS integration, please contact the repository maintainers.

