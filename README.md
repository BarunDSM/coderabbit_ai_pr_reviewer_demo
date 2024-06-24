# Coderabbit ai_pr_reviewer

## Overview

CodeRabbit `ai-pr-reviewer` is an AI-based code reviewer and summarizer for
GitHub pull requests using OpenAI's `gpt-3.5-turbo` and `gpt-4` models. It is
designed to be used as a GitHub Action and can be configured to run on every
pull request and review comments.

## Install instructions

`ai-pr-reviewer` runs as a GitHub Action. Add the below file to your repository
at `.github/workflows/ai-pr-reviewer.yml`, you may set the features true according to your need

```yaml
name: Code Review

permissions:
  contents: read
  pull-requests: write

on:
  pull_request:
  pull_request_review_comment:
    types: [created]

concurrency:
  group:
    ${{ github.repository }}-${{ github.event.number || github.head_ref ||
    github.sha }}-${{ github.workflow }}-${{ github.event_name ==
    'pull_request_review_comment' && 'pr_comment' || 'pr' }}
  cancel-in-progress: ${{ github.event_name != 'pull_request_review_comment' }}

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: coderabbitai/ai-pr-reviewer@latest
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        with:
          debug: false
          review_simple_changes: false
          review_comment_lgtm: false
```

#### Environment variables

- `GITHUB_TOKEN`: This should already be available to the GitHub Action
  environment. This is used to add comments to the pull request.
- `OPENAI_API_KEY`: use this to authenticate with OpenAI API. You can get one
  [here](https://platform.openai.com/account/api-keys).
  
  Please add these keys to your GitHub Action secrets.


### Prompts & Configuration

To get an idea of all actions,see: [action.yml](actions.yml), then you may add/change these action under jobs(with) section in the workflow.

**Following are some prompt suggestions that you may take reference from**:


<details>
<summary>Reviewer Prompt</summary>

```yaml
system_message: |
  You are `@coderabbitai` (aka `github-actions[bot]`), a language model
  trained by OpenAI. Your purpose is to act as a highly experienced
  DevRel (developer relations) professional with focus on cloud-native
  infrastructure.

  Company context -
  CodeRabbit is an AI-powered Code reviewer.It boosts code quality and cuts manual effort. Offers context-aware, line-by-line feedback, highlights critical changes,
  enables bot interaction, and lets you commit suggestions directly from GitHub.

  When reviewing or generating content focus on key areas such as -
  - Accuracy
  - Relevance
  - Clarity
  - Technical depth
  - Call-to-action
  - SEO optimization
  - Brand consistency
  - Grammar and prose
  - Typos
  - Hyperlink suggestions
  - Graphics or images (suggest Dall-E image prompts if needed)
  - Empathy
  - Engagement
```

</details>

<details>
<summary>Add your own personal summaizer</summary>

```yaml
# Note: Apart from the default summary provided by coderabbit, you can add your own with prompts of your choice 
summarize: |
  Provide your final response in markdown with the following content:
  
  - **Walkthrough**: A high-level summary of the overall change instead of 
  specific files within max 150 words.
  - **Changes**: A markdown table of files and their summaries, including a short summary of what the added or 
  changed functionalities/code do to help the developer get a clear understanding of the changes. 
  Group files with similar changes together into a single row to save space.
            
  
  Avoid additional commentary as this summary will be added as a comment on the 
  GitHub pull request. Use the titles "Walkthrough" and "Changes" and they must be H2.
```

</details>

### CodeRabbit Configration File (`.coderabbit.yaml`)

- You can programmatically configure CodeRabbit by adding a `.coderabbit.yaml` file to the root of your repository.
- Please see the [configuration documentation](https://docs.coderabbit.ai/guides/configure-coderabbit) for more information.
- If your editor has YAML language server enabled, you can add the path at the top of this file to enable auto-completion and validation: `# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json`


<details>
<summary>Tips to chat with CodeRabbit</summary>

There are 3 ways to chat with [CodeRabbit](https://coderabbit.ai):

- Review comments: Directly reply to a review comment made by CodeRabbit. Example:
	- `I pushed a fix in commit <commit_id>.`
	- `Generate unit testing code for this file.`
	- `Open a follow-up GitHub issue for this discussion.`
- Files and specific lines of code (under the "Files changed" tab): Tag `@coderabbitai` in a new review comment at the desired location with your query. Examples:
	- `@coderabbitai generate unit testing code for this file.`
	-	`@coderabbitai modularize this function.`
- PR comments: Tag `@coderabbitai` in a new PR comment to ask questions about the PR branch. For the best results, please provide a very specific query, as very limited context is provided in this mode. Examples:
	- `@coderabbitai generate interesting stats about this repository and render them as a table.`
	- `@coderabbitai show all the console.log statements in this repository.`
	- `@coderabbitai read src/utils.ts and generate unit testing code.`
	- `@coderabbitai read the files in the src/scheduler package and generate a class diagram using mermaid and a README in the markdown format.`
	- `@coderabbitai help me debug CodeRabbit configuration file.`

Note: Be mindful of the bot's finite context window. It's strongly recommended to break down tasks such as reading entire modules into smaller chunks. For a focused discussion, use review comments to chat about specific files and their changes, instead of using the PR comments.

### CodeRabbit Commands (invoked as PR comments)

- `@coderabbitai pause` to pause the reviews on a PR.
- `@coderabbitai resume` to resume the paused reviews.
- `@coderabbitai review` to trigger an incremental review. This is useful when automatic reviews are disabled for the repository.
- `@coderabbitai full review` to do a full review from scratch and review all the files again.
- `@coderabbitai summary` to regenerate the summary of the PR.
- `@coderabbitai resolve` resolve all the CodeRabbit review comments.
- `@coderabbitai configuration` to show the current CodeRabbit configuration for the repository.
- `@coderabbitai help` to get help.


Additionally, you can add `@coderabbitai ignore` anywhere in the PR description to prevent this PR from being reviewed.

</details>

<!-- tips_end -->

### Documentation 

- Visit CodeRabbit's documentation [Documentation](https://coderabbit.ai/docs) for detailed information on how to use CodeRabbit.
