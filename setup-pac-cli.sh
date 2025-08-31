#!/bin/zsh

# Your script is now idempotent. It checks for existing plugins, SDKs, and tools before installing or updating, so running it multiple times will not cause duplicate installations or unwanted changes.
echo "\nScript: setup-pac-cli.sh"
echo "This script is idempotent.\n"

# setup-pac-cli.sh
#
# Summary: This script automates the setup of the .NET SDK environment using asdf and DotNet CLI.
# It installs the preferred and fallback .NET SDK versions, adds the dotnet plugin to asdf, and 
# ensures the environment is ready for development or CI/CD workflows.
#
 # Applications and Commands Used:
 # - asdf: Universal version manager for installing and managing .NET SDK versions.
 #   - asdf plugin add dotnet: Adds the dotnet plugin for asdf.
 #   - asdf install dotnet <version>: Installs specified .NET SDK version.
 #   - asdf set dotnet <version>: Sets the active .NET SDK version for the directory.

 # - dotnet: .NET CLI for verifying installation and installing global tools.
 #   - dotnet --version: Checks installed .NET SDK version.
 #   - dotnet tool install --global Microsoft.PowerApps.CLI.Tool: Installs the PowerApps CLI globally.

 # - PAC CLI (Microsoft.PowerApps.CLI.Tool): Command-line tool for Power Platform development.

 # - .tool-versions: File used by asdf to specify tool versions for the project.
 # - set-dotnet-env.zsh: Script sourced to set environment variables for dotnet.





# Exit on error
set -e

# Preferred and fallback .NET SDK versions
PREFERRED_DOTNET_VERSION="9.0.304"
FALLBACK_DOTNET_VERSION="8.0.100"


# Add dotnet plugin only if not already added
if ! asdf plugin list | grep -q "dotnet"; then
  echo "🔧 Adding dotnet plugin to asdf (hensou/asdf-dotnet)..."
  asdf plugin add dotnet https://github.com/hensou/asdf-dotnet
else
  echo "dotnet plugin already added."
fi


# Install preferred .NET SDK only if not already installed
if ! asdf list dotnet | grep -q "$PREFERRED_DOTNET_VERSION"; then
  echo "📦 Installing preferred .NET SDK version $PREFERRED_DOTNET_VERSION..."
  asdf install dotnet $PREFERRED_DOTNET_VERSION
else
  echo ".NET SDK $PREFERRED_DOTNET_VERSION already installed."
fi

# Set .NET SDK version only if not already set
current_dotnet_version=$(asdf current dotnet | awk '{print $2}')
if [ "$current_dotnet_version" != "$PREFERRED_DOTNET_VERSION" ]; then
  echo "📦 Setting .NET SDK version $PREFERRED_DOTNET_VERSION for current directory..."
  asdf set dotnet $PREFERRED_DOTNET_VERSION
  echo "dotnet $PREFERRED_DOTNET_VERSION" > .tool-versions
else
  echo ".NET SDK version already set to $PREFERRED_DOTNET_VERSION."
fi


echo "🔧 Sourcing environment variables for dotnet..."
. ~/.asdf/plugins/dotnet/set-dotnet-env.zsh

echo "✅ Verifying dotnet installation..."
dotnet_version=$(dotnet --version)
echo "Installed .NET version: $dotnet_version"


# Install PAC CLI only if not already installed
if dotnet tool list --global | grep -q "Microsoft.PowerApps.CLI.Tool"; then
  echo "PAC CLI already installed globally."
else
  echo "🚀 Attempting PAC CLI install with .NET $dotnet_version..."
  if dotnet tool install --global Microsoft.PowerApps.CLI.Tool; then
    echo "🎉 PAC CLI installed successfully with .NET $dotnet_version"
  else
    echo "⚠️ PAC CLI failed to install with .NET $dotnet_version. Falling back to .NET $FALLBACK_DOTNET_VERSION..."
    if ! asdf list dotnet | grep -q "$FALLBACK_DOTNET_VERSION"; then
      asdf install dotnet $FALLBACK_DOTNET_VERSION
    fi
    asdf set dotnet $FALLBACK_DOTNET_VERSION
    echo "dotnet $FALLBACK_DOTNET_VERSION" > .tool-versions
    . ~/.asdf/plugins/dotnet/set-dotnet-env.zsh
    dotnet tool install --global Microsoft.PowerApps.CLI.Tool
    echo "✅ PAC CLI installed with fallback .NET version $FALLBACK_DOTNET_VERSION"
  fi
fi


echo "📁 Ensuring ~/.dotnet/tools is in PATH..."
if ! grep -q 'export PATH="$HOME/.dotnet/tools:$PATH"' ~/.zshrc; then
  echo 'export PATH="$HOME/.dotnet/tools:$PATH"' >> ~/.zshrc
  echo "Added ~/.dotnet/tools to PATH in ~/.zshrc"
else
  echo "~/.dotnet/tools is already in PATH"
fi
