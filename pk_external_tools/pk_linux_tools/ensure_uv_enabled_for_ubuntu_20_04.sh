#!/bin/bash

set -e

echo "🛠 Installing prerequisites..."
sudo apt update
sudo apt install -y curl bash

echo "📦 Downloading and installing uv..."
curl -Ls https://astral.sh/uv/install.sh | bash

echo "🔧 Configuring PATH..."

# Update PATH in the current shell
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

# Persist PATH updates in ~/.bashrc if not already present
if ! grep -q 'export PATH="\$HOME/.local/bin:\$PATH"' ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'Added ~/.local/bin to PATH in ~/.bashrc'
fi

if ! grep -q 'export PATH="\$HOME/.cargo/bin:\$PATH"' ~/.bashrc; then
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
    echo 'Added ~/.cargo/bin to PATH in ~/.bashrc'
fi

# 🧠 Ensure current shell knows about uv
echo "🔁 Rehashing shell to pick up new binaries..."
hash -r 2>/dev/null || true

# Also double-check manually
if ! command -v uv >/dev/null 2>&1; then
    echo "⚠️ uv not found in PATH, attempting manual source of binary"
    if [ -f "$HOME/.local/bin/uv" ]; then
        echo "🟢 uv is installed at $HOME/.local/bin/uv"
        echo "Try running: export PATH=\$HOME/.local/bin:\$PATH"
    else
        echo "❌ uv binary not found. Something went wrong."
        exit 1
    fi
fi

echo "✅ Checking uv version..."
uv --version

echo "🎉 uv is successfully installed and ready to use!"
