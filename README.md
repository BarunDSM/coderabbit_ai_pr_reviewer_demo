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
<summary>Blog Reviewer Prompt</summary>

```yaml
summarize: Provide your final response in markdown with the following content:

      - **Walkthrough**: A high-level summary of the overall change instead of 
        specific files within 80 words.
      - **Changes**: A markdown table of files and their summaries. Group files 
        with similar changes together into a single row to save space.
      - **Poem**: Below the changes, include a whimsical, short poem written by 
        a rabbit to celebrate the changes. Format the poem as a quote using 
        the ">" symbol and feel free to use emojis where relevant.

      Avoid additional commentary as this summary will be added as a comment on the 
      GitHub pull request. Use the titles "Walkthrough" and "Changes" and they must be H2.
```

</details>


<details>
<summary>Summary without poem</summary>

```yaml
# Note: This will only work if you have added summary under the jobs(with) section of the workflow and will not change the default code rabbit response
summarize: |
      Provide your final response in markdown with the following content:

      - **Walkthrough**: A high-level summary of the overall change instead of 
        specific files within 80 words.
      - **Changes**: A markdown table of files and their summaries. Group files 
        with similar changes together into a single row to save space.

      ## simply remove poem section from here, check summarize in action.yml

      Avoid additional commentary as this summary will be added as a comment on the 
      GitHub pull request. Use the titles "Walkthrough" and "Changes" and they must be H2.
```

</details>
