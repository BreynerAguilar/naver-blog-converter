#!/bin/bash
# Naver Blog Converter 설치 스크립트
# Installation script for Naver Blog Converter

set -e

echo "=========================================="
echo "네이버 블로그 변환기 설치"
echo "Naver Blog Converter Installation"
echo "=========================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv가 설치되지 않았습니다."
    echo "❌ uv is not installed."
    echo ""
    echo "uv 설치 방법 / Install uv:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

echo "✓ uv 발견됨 / uv found"
echo ""

# Install Python dependencies
echo "1️⃣  Python 의존성 설치 중..."
echo "   Installing Python dependencies..."
uv sync
echo "✓ Python 의존성 설치 완료"
echo ""

# Check for gcloud
echo "2️⃣  Google Cloud CLI 확인 중..."
echo "   Checking for Google Cloud CLI..."
if ! command -v gcloud &> /dev/null; then
    echo "⚠️  gcloud CLI가 설치되지 않았습니다."
    echo "⚠️  gcloud CLI is not installed."
    echo ""
    echo "GCS 자동 업로드를 위해 gcloud CLI가 필요합니다."
    echo "gcloud CLI is required for automatic GCS upload."
    echo ""
    echo "설치 방법 / Installation:"
    echo "  https://cloud.google.com/sdk/docs/install"
    echo ""
    echo "설치 후 인증 / After installation, authenticate:"
    echo "  gcloud auth application-default login"
    echo "  gcloud config set project YOUR-PROJECT-ID"
    echo ""
else
    echo "✓ gcloud CLI 발견됨 / gcloud CLI found"

    # Prompt for authentication
    echo ""
    read -p "Google Cloud 인증을 진행하시겠습니까? (y/n) / Authenticate with Google Cloud? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gcloud auth application-default login

        echo ""
        read -p "GCP 프로젝트 ID를 입력하세요 / Enter your GCP project ID: " project_id
        if [ -n "$project_id" ]; then
            gcloud config set project "$project_id"

            # Create .env file
            if [ ! -f .env ]; then
                echo "GCS_PROJECT_ID=$project_id" > .env
                echo "GCS_BUCKET_NAME=${project_id}-naverblog" >> .env
                echo "GCS_LOCATION=ASIA-NORTHEAST3" >> .env
                echo "GCS_SUBFOLDER=naverblog" >> .env
                echo "✓ .env 파일 생성됨 / .env file created"
            fi
        fi
    fi
fi
echo ""

# Check for mmdc (mermaid-cli)
echo "3️⃣  Mermaid CLI 확인 중..."
echo "   Checking for Mermaid CLI..."
if ! command -v mmdc &> /dev/null; then
    echo "⚠️  mmdc (mermaid-cli)가 설치되지 않았습니다."
    echo "⚠️  mmdc (mermaid-cli) is not installed."
    echo ""
    echo "Mermaid 다이어그램 자동 렌더링을 위해 필요합니다 (선택사항)."
    echo "Required for automatic mermaid diagram rendering (optional)."
    echo ""
    echo "설치 방법 / Installation:"
    echo "  npm install -g @mermaid-js/mermaid-cli"
    echo ""
    echo "또는 수동 렌더링 / Or manual rendering:"
    echo "  https://mermaid.live/"
    echo ""
else
    echo "✓ Mermaid CLI 발견됨 / Mermaid CLI found"
fi
echo ""

# Ask about Claude Code integration
echo "4️⃣  Claude Code 슬래시 커맨드 설치"
echo "   Claude Code slash command installation"
echo ""
read -p "Claude Code 슬래시 커맨드를 설치하시겠습니까? (y/n) / Install Claude Code slash command? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Obsidian 볼트 경로를 입력하세요 / Enter your Obsidian vault path: " vault_path

    if [ -n "$vault_path" ] && [ -d "$vault_path" ]; then
        # Create .claude/commands directory if it doesn't exist
        mkdir -p "$vault_path/.claude/commands"

        # Copy naver.md command
        if [ -f "commands/naver.md" ]; then
            cp commands/naver.md "$vault_path/.claude/commands/"
            echo "✓ /naver 커맨드가 설치되었습니다."
            echo "✓ /naver command installed."
            echo "  위치 / Location: $vault_path/.claude/commands/naver.md"
        else
            echo "⚠️  commands/naver.md 파일을 찾을 수 없습니다."
            echo "⚠️  commands/naver.md file not found."
        fi
    else
        echo "⚠️  유효하지 않은 경로입니다."
        echo "⚠️  Invalid path."
    fi
fi
echo ""

# Test installation
echo "5️⃣  설치 테스트 중..."
echo "   Testing installation..."
if uv run python -c "import markdown; from bs4 import BeautifulSoup; print('✓ Dependencies OK')" 2>/dev/null; then
    echo "✓ 설치 테스트 통과 / Installation test passed"
else
    echo "❌ 설치 테스트 실패 / Installation test failed"
    echo "   'uv sync'를 다시 실행해보세요 / Try running 'uv sync' again"
    exit 1
fi
echo ""

echo "=========================================="
echo "✅ 설치 완료!"
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "다음 단계 / Next steps:"
echo ""
echo "1️⃣  마크다운 파일 변환 / Convert a markdown file:"
echo "   uv run python md2naver.py your-file.md --gcs"
echo ""
echo "2️⃣  Claude Code에서 사용 (설치한 경우) / Use in Claude Code (if installed):"
echo "   /naver \"your-file.md\""
echo ""
echo "3️⃣  도움말 보기 / View help:"
echo "   uv run python md2naver.py --help"
echo ""
echo "4️⃣  문서 읽기 / Read documentation:"
echo "   cat README_KR.md"
echo ""
echo "=========================================="
echo "즐거운 블로깅 되세요! 🚀"
echo "Happy blogging! 🚀"
echo "=========================================="
