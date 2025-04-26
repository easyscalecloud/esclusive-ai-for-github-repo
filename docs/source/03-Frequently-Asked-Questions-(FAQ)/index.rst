.. _faq:

Frequently Asked Questions (FAQ)
===============================================================================

General Questions
-------------------------------------------------------------------------------

What is ESClusive AI for GitHub Repo?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ESClusive AI for GitHub Repo is a tool that automates the creation of knowledge base files from your GitHub repository. These knowledge base files capture essential information about your codebase, which can be used with any AI assistant (like ChatGPT, Claude, or Gemini) to enhance their understanding of your specific project structure, patterns, and architecture.

How does ESClusive AI work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ESClusive AI works through a GitHub Action that:

1. Scans your repository based on the include/exclude patterns you specify
2. Extracts relevant files and their content
3. Processes the content into a structured knowledge base format
4. Publishes the resulting knowledge base file(s) as GitHub release assets
5. Makes them available for download and use with any AI assistant

Why would I need ESClusive AI for my repository?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ESClusive AI solves the fundamental disconnect between AI assistants and your unique codebase. Without proper context, AI assistants provide generic suggestions that don't align with your project's architecture and patterns. By using ESClusive AI, you'll get:

- AI responses that understand your specific project structure
- Suggestions that follow your established coding patterns
- More accurate help with debugging and implementation
- Faster onboarding for new team members
- Better documentation assistance tailored to your codebase

What makes ESClusive AI different from other AI coding tools?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ESClusive AI stands apart from other AI coding tools in several key ways:

- **Universal Compatibility**: Works with ANY AI assistant, not locked to a specific provider
- **Zero Integration Complexity**: No APIs, tokens, or complex configurations required
- **Complete User Control**: You decide exactly which files to include in your knowledge base
- **No Ongoing Costs**: Generate knowledge base files as needed without subscription fees
- **Security-Focused**: Your code never leaves your control - just download and use the knowledge base file

Setup and Configuration
-------------------------------------------------------------------------------

How do I set up ESClusive AI for my GitHub repository?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Setting up ESClusive AI is a simple 3-step process:

1. Create a GitHub Action workflow file at ``.github/workflows/run_esclusive_ai_for_github_repo.yml``
2. Create a configuration file at ``.github/workflows/esclusive_ai_for_github_repo_config.json``
3. Run the workflow through GitHub Actions and download your knowledge base file(s)

Detailed setup instructions are available in the :ref:`5minutes-setup-guide`.

What files should I include in my knowledge base?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For optimal results, include files that define your project's:

- Core functionality (e.g., Python/JavaScript/TypeScript files)
- Architecture documentation
- API definitions
- README files
- Design documents

It's generally best to exclude:

- Virtual environments (``.venv``, ``venv``)
- Dependency directories (``node_modules``)
- Build artifacts and cache directories
- Large binary files or datasets

Can I create multiple knowledge bases for different aspects of my project?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes! You can define multiple document groups in your configuration file, each with its own include/exclude patterns. For example:

.. code-block:: javascript

    {
        "document_groups": [
            {
                "name": "all",
                "include": ["**/*.py", "**/*.md"],
                "exclude": [".venv"]
            },
            {
                "name": "frontend",
                "include": ["frontend/**/*.js", "frontend/**/*.ts"],
                "exclude": ["node_modules"]
            },
            {
                "name": "docs",
                "include": ["docs/**/*.md", "**/*.rst"],
                "exclude": []
            }
        ]
    }

Each document group will generate a separate knowledge base file.

How do the include/exclude patterns work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The include/exclude patterns follow the same syntax as ``.gitignore`` files. Here are some examples:

- ``**/*.py`` - Match all Python files in any directory
- ``src/*.js`` - Match JavaScript files directly in the src directory
- ``docs/source/**/*.rst`` - Match all reStructuredText files under docs/source
- ``tmp/`` - Match all files inside directories named tmp

For detailed pattern matching information, refer to the :ref:`include-exclude-patterns`.

Does ESClusive AI work with private repositories?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, ESClusive AI works with both public and private GitHub repositories. The GitHub Action runs within your repository's context, so it has access to private repositories when properly configured with the necessary permissions.

Usage and Integration
-------------------------------------------------------------------------------

How do I use the knowledge base file with an AI assistant?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Using your knowledge base file is incredibly simple:

1. Download the knowledge base file(s) from your GitHub repository's "knowledge-base" release
2. Open a chat with your preferred AI assistant (Claude, ChatGPT, Gemini, etc.)
3. Drag and drop the knowledge base file into the chat window
4. Start asking questions about your codebase

The AI will now have context about your specific project structure and patterns.

Will this work with any AI assistant?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes! The knowledge base file format is designed to be universal and compatible with any text-based AI assistant, including:

- Claude (Anthropic)
- ChatGPT / GPT-4 (OpenAI)
- Gemini (Google)
- Enterprise AI systems
- Any other text-based AI assistant that can accept file uploads

How large can my knowledge base file be?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The size of your knowledge base file depends on the amount of content in your repository and your include/exclude patterns. Most AI assistants have limits on the size of files they can process:

- Claude: Up to 10MB
- ChatGPT Plus: Up to 2MB for GPT-4
- Gemini: Around 2MB

If your knowledge base exceeds these limits, consider using real knowledge base such as ChatGPT Project or Claude Project instead of dropping the all-in-one knowledge base file into the chat.

Can I automate knowledge base updates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes! You can configure your workflow to automatically trigger knowledge base generation whenever changes are pushed to your repository. In your workflow file, uncomment the push/pull_request triggers:

.. code-block:: yaml

    on:
      push:
        branches: ["main"]
      pull_request:
        branches: ["main"]
      workflow_dispatch:

This ensures your knowledge base stays up-to-date with your codebase.

Does the knowledge base file contain my actual source code?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, the knowledge base file contains the actual content of the files you've included, processed into a structured format that AI assistants can understand. This is what enables the AI to provide context-aware assistance specific to your codebase.

If you have sensitive information, be careful about which files you include and who you share the knowledge base file with.

Technical and Security
-------------------------------------------------------------------------------

Is my code secure when using ESClusive AI?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ESClusive AI is designed with security in mind:

1. The GitHub Action runs entirely within your GitHub Actions environment
2. No code is sent to external servers for processing
3. You control exactly which files are included in the knowledge base
4. The knowledge base file remains in your GitHub repository as a release asset
5. You decide when and with whom to share the knowledge base file

This approach gives you complete control over your code and how it's used.

What permissions does the GitHub Action require?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The GitHub Action requires the ``contents: write`` permission to publish the knowledge base file as a GitHub release asset. This is specified in the workflow file:

.. code-block:: yaml

    permissions:
      contents: write

No other permissions are needed for the basic functionality.

Can I use this with GitHub Enterprise?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, but need additional setup.

Which file formats are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ESClusive AI can process any text-based file format. Common formats include:

- Programming languages (Python, JavaScript, TypeScript, etc.)
- Markup languages (Markdown, reStructuredText, etc.)
- Configuration files (JSON, YAML, etc.)
- Documentation files

Binary files are not recommended as they won't provide useful context to AI assistants.

How does ESClusive AI handle large repositories?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For large repositories, consider these best practices:

1. Be more selective with your include/exclude patterns
2. Create multiple document groups focused on specific components
3. Exclude test data, build artifacts, and automatically generated files
4. Consider increasing the GitHub Actions timeout if needed for very large repositories

Miscellaneous
-------------------------------------------------------------------------------

Is ESClusive AI free to use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, ESClusive AI is free to use and is released under the AGPL-3.0 license. There are no subscription fees or usage limits imposed by the tool itself. Your only costs are those associated with running GitHub Actions, which are free for public repositories and come with a free allocation for private repositories.

Where can I get help if I have issues?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you need help with ESClusive AI, you can:

1. Join the `Gitter chat channel <https://matrix.to/#/!VvBAFlTNlUtAaqMomD:gitter.im?via=gitter.im>`_ for direct support
2. Check the `documentation <https://esclusive-ai-for-github-repo.easyscalecloud.com/>`_
3. Open an issue in the `GitHub repository <https://github.com/easyscalecloud/esclusive-ai-for-github-repo/issues/new>`_

Can I contribute to ESClusive AI?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes! ESClusive AI is an open-source project and welcomes contributions. You can:

1. Fork the repository
2. Submit pull requests
3. Report bugs
4. Suggest features
5. Improve documentation

Check the project's GitHub repository for contribution guidelines.
