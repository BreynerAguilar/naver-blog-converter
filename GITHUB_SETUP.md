# GitHub 저장소 생성 및 배포 가이드

## 1. GitHub에서 새 저장소 생성

1. https://github.com/new 방문
2. 저장소 이름: `naver-blog-converter`
3. 설명: "Convert Obsidian markdown with mermaid diagrams to Naver blog compatible HTML"
4. Public 선택
5. **README는 추가하지 말 것** (이미 있음)
6. Create repository 클릭

## 2. 로컬 저장소 초기화 및 푸시

```bash
cd /Users/julius/Documents/naver_blog

# Git 초기화 (이미 되어있으면 생략)
git init

# 원격 저장소 추가 (juliuschun을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/juliuschun/naver-blog-converter.git

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Naver Blog Converter with GCS support

- Markdown to HTML converter optimized for Naver Blog
- Automatic mermaid diagram rendering to PNG
- Google Cloud Storage integration for image hosting
- Claude Code slash command support
- Korean documentation (README_KR.md)
- Installation script (install.sh)
- MIT License"

# 메인 브랜치로 푸시
git branch -M main
git push -u origin main
```

## 3. README 업데이트

GitHub에서 juliuschun 부분을 실제 사용자명으로 변경:

### 파일 목록
- `README.md` (한국어)
- `README_EN.md` (영어)
- `commands/naver.md`
- `CONTRIBUTING.md`
- `install.sh`

찾아서 변경:
```
juliuschun → 실제_사용자명
```

## 4. Topics 추가

저장소 페이지에서:
1. About 섹션의 ⚙️ 아이콘 클릭
2. Topics 추가:
   - `naver-blog`
   - `markdown-converter`
   - `mermaid`
   - `obsidian`
   - `claude-code`
   - `python`
   - `gcs`
   - `korean`

## 5. GitHub Pages 설정 (선택사항)

문서 호스팅:
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, /docs 또는 /
4. Save

## 6. 릴리스 생성

첫 번째 릴리스:
1. Releases → Create a new release
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Release`
4. Description:
```markdown
## 첫 번째 릴리스 🎉

### 주요 기능
- ✅ Mermaid 다이어그램 자동 PNG 변환
- ✅ Google Cloud Storage 자동 업로드
- ✅ 네이버 블로그 최적화 HTML 생성
- ✅ Claude Code 슬래시 커맨드 지원
- ✅ 한국어 문서

### 설치
\`\`\`bash
git clone https://github.com/juliuschun/naver-blog-converter.git
cd naver-blog-converter
./install.sh
\`\`\`

### 사용법
\`\`\`bash
uv run python md2naver.py your-file.md --gcs
\`\`\`

자세한 내용은 [README.md](https://github.com/juliuschun/naver-blog-converter/blob/main/README.md) 참조
```

5. Publish release

## 7. README 뱃지 추가 (선택사항)

`README.md` 상단에 추가:

```markdown
# 네이버 블로그 변환기

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub stars](https://img.shields.io/github/stars/juliuschun/naver-blog-converter)
![GitHub issues](https://img.shields.io/github/issues/juliuschun/naver-blog-converter)
```

## 8. 사용자 가이드

### 다른 사용자가 설치하는 방법

```bash
# 저장소 복제
git clone https://github.com/juliuschun/naver-blog-converter.git
cd naver-blog-converter

# 설치 스크립트 실행
./install.sh

# 사용
uv run python md2naver.py your-article.md --gcs
```

### Claude Code 사용자용

1. 저장소 복제
2. `install.sh` 실행하고 Obsidian 볼트 경로 입력
3. Claude Code에서 `/naver` 명령 사용

## 9. CI/CD 설정 (선택사항)

`.github/workflows/test.yml` 생성:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync
      - name: Test imports
        run: uv run python -c "import markdown; from bs4 import BeautifulSoup; print('OK')"
```

## 10. 홍보

### 공유할 곳
- Naver 블로그 카페/커뮤니티
- Obsidian 한국 커뮤니티
- Reddit r/ObsidianMD
- Twitter/X
- 개발자 커뮤니티 (OKKY, GeekNews 등)

### 샘플 소개글
```
네이버 블로그에 Mermaid 다이어그램이 포함된 마크다운을 올리는 게 어려우셨나요?

이제 한 번의 명령으로 자동 변환!
- Mermaid → PNG 자동 렌더링
- Google Cloud Storage 자동 업로드
- 복사-붙여넣기만 하면 끝!

GitHub: https://github.com/juliuschun/naver-blog-converter
```

## 완료!

이제 저장소가 공개되었습니다. 사용자들이:
1. `git clone`으로 다운로드
2. `./install.sh`로 설치
3. `uv run python md2naver.py`로 사용
4. Claude Code에서 `/naver` 명령 사용

가능합니다!
