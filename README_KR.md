# 네이버 블로그 변환기 (Naver Blog Converter)

Obsidian 마크다운 파일을 네이버 블로그 호환 HTML로 자동 변환하는 도구입니다. Mermaid 다이어그램을 PNG 이미지로 렌더링하고 Google Cloud Storage에 자동 업로드합니다.

## 주요 기능

✅ **Mermaid 다이어그램 자동 렌더링** - PNG 이미지로 변환
✅ **Google Cloud Storage 자동 업로드** - 이미지 URL 수동 교체 불필요
✅ **한 번의 명령으로 변환** - 마크다운에서 복사-붙여넣기 가능한 HTML까지
✅ **테이블 HTML 변환** - 아름다운 스타일 적용
✅ **Frontmatter 제거** 및 WikiLink 변환
✅ **코드 블록 보존** - Color Scripter 연동 가능
✅ **Claude Code 슬래시 커맨드** - `/naver` 명령으로 간편 실행

## 빠른 시작

### 1. 저장소 복제

```bash
git clone https://github.com/juliuschun/naver-blog-converter.git
cd naver-blog-converter
```

### 2. 설치 스크립트 실행

```bash
./install.sh
```

설치 스크립트는 다음을 수행합니다:
- Python 의존성 설치 (uv 사용)
- Google Cloud 인증 설정
- Claude Code 슬래시 커맨드 설치 (선택사항)
- Mermaid CLI 설치 안내

### 3. 사용법

```bash
# GCS 자동 업로드와 함께 변환
uv run python md2naver.py "your-file.md" --gcs

# 출력 디렉토리 지정
uv run python md2naver.py "your-file.md" --gcs -o custom_output
```

## Claude Code에서 사용하기

설치 후 Obsidian 볼트에서 사용 가능:

```
/naver "1011 산일전기와 전력 시장 공급망 분석.md"
```

Claude가 자동으로:
- 볼트에서 파일 찾기
- GCS 업로드와 함께 변환
- 결과 요약 표시
- 다음 단계 안내

## 작동 원리

### `--gcs` 플래그 사용 시

1. **렌더링** - Mermaid 다이어그램을 PNG로 변환
2. **업로드** - PNG를 Google Cloud Storage에 자동 업로드
3. **생성** - 실제 GCS URL이 포함된 HTML 생성
4. **출력** - 바로 복사-붙여넣기 가능한 HTML 파일

**결과:** 플레이스홀더 없음, 수동 작업 없음 - 그냥 복사해서 붙여넣기!

## 출력 파일

각 변환은 다음을 생성합니다:

```
naver_파일명_20251012_170704/
├── 파일명.html                    # 네이버 블로그에 붙여넣기 준비 완료
├── 파일명_INSTRUCTIONS.md         # 수동 단계 (필요시)
├── mermaid_code.txt               # Mermaid 소스 백업
└── images/                        # PNG 파일 (GCS에도 업로드됨)
    ├── mermaid_1.png
    ├── mermaid_2.png
    └── ...
```

## 지원하는 마크다운 기능

| 기능 | 상태 | 비고 |
|------|------|------|
| 헤더 (H1-H6) | ✅ | 완전 지원 |
| 굵게/기울임 | ✅ | 인라인 스타일로 강제 적용 |
| 목록 | ✅ | 완전 지원 |
| 테이블 | ✅ | 아름다운 스타일의 HTML로 변환 |
| 코드 블록 | ✅ | 보존, Color Scripter 연동 가능 |
| 인용구 | ✅ | 완전 지원 |
| 링크 | ✅ | 완전 지원 |
| 이미지 (외부) | ✅ | 완전 지원 |
| **Mermaid 다이어그램** | ✅ | **PNG로 변환, GCS 자동 업로드** |
| WikiLinks `[[링크]]` | ⚠️ | 일반 텍스트로 변환 |
| YAML frontmatter | ⚠️ | 제거됨 |

## Google Cloud Storage 설정

### 1회 설정 (처음만)

```bash
# gcloud CLI 설치
# https://cloud.google.com/sdk/docs/install

# 인증
gcloud auth application-default login

# 프로젝트 설정 (본인의 GCP 프로젝트 ID로 변경)
gcloud config set project YOUR-PROJECT-ID
```

### 설정 사용자화

`.env` 파일 생성:

```bash
cp .env.example .env
nano .env
```

값 수정:

```env
GCS_PROJECT_ID=your-project-id
GCS_BUCKET_NAME=your-bucket-name
GCS_LOCATION=ASIA-NORTHEAST3  # 서울
```

## 네이버 블로그에 붙여넣기

1. **열기** - 생성된 `파일명.html` 파일
2. **복사** - 전체 선택 (Cmd+A, Cmd+C)
3. **붙여넣기** - 네이버 블로그 에디터에 붙여넣기
4. **완료!** - 이미지가 즉시 표시됨

### DevTools 방법 (권장)

1. 네이버 블로그 글쓰기 열기
2. F12 눌러 DevTools 열기
3. Elements 패널에서 편집 가능한 div 찾기
4. 우클릭 → Edit as HTML
5. `output.html`의 HTML 붙여넣기
6. DevTools 닫기
7. 미리보기 후 발행

## GCS 이미지 URL

이미지는 다음 주소로 접근 가능:
```
https://storage.googleapis.com/your-bucket-name/naverblog/mermaid_1.png
```

- **공개:** 누구나 볼 수 있음 (네이버 블로그에 필요)
- **영구적:** URL이 만료되지 않음
- **빠름:** Google CDN 제공
- **비용:** 무료 티어로 일반 사용량 충분

## 비용 추정

**무료 티어:**
- 5GB 저장 공간/월 (무료)
- 1GB 송신 (무료)

**사용량 예시 (월 10개 블로그 포스트):**
- 이미지당 ~100KB × 8개 이미지 × 10개 포스트 = ~8MB 저장
- 최소 송신량 (방문자가 이미지 보기)

**결과:** 무료 티어 내! (~$0/월)

## 문제 해결

### "Permission denied" 또는 "401 Unauthorized"

재인증:
```bash
gcloud auth application-default login
```

### "Module not found: google.cloud"

의존성 설치:
```bash
uv sync
```

### "mmdc not found" (mermaid 렌더링 실패)

Mermaid CLI 설치:
```bash
npm install -g @mermaid-js/mermaid-cli
```

또는 https://mermaid.live/ 에서 수동 렌더링

### 네이버에서 이미지가 표시되지 않음

1. 버킷이 공개인지 확인 (변환기가 자동으로 설정)
2. URL이 브라우저에서 작동하는지 확인
3. "Step 7.6: GCS URL로 플레이스홀더 교체" 후의 HTML을 복사했는지 확인

## 명령줄 옵션

```bash
# 기본 사용법
uv run python md2naver.py INPUT.md

# GCS 업로드와 함께
uv run python md2naver.py INPUT.md --gcs

# 사용자 지정 출력 디렉토리
uv run python md2naver.py INPUT.md -o my_output

# 다른 GCS 프로젝트/버킷
uv run python md2naver.py INPUT.md --gcs \
  --gcs-project other-project \
  --gcs-bucket other-bucket
```

## 프로젝트 구조

```
naver-blog-converter/
├── md2naver.py              # 메인 변환기
├── gcs_uploader.py          # GCS 업로드 모듈
├── update_image_urls.py     # URL 수동 교체 헬퍼
├── config.py                # 설정 관리
├── install.sh               # 설치 스크립트
├── pyproject.toml           # 의존성
├── .env.example             # 설정 템플릿
├── README_KR.md             # 한국어 문서 (이 파일)
├── README.md                # 영어 문서
└── docs/                    # 추가 문서
    ├── GCS_SETUP.md         # GCS 상세 설정
    ├── QUICKSTART_GCS.md    # GCS 빠른 가이드
    └── CLAUDE_CODE.md       # Claude Code 연동
```

## 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 기여

이슈와 풀 리퀘스트를 환영합니다!

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. 풀 리퀘스트 열기

## 리소스

- **Mermaid Live Editor:** https://mermaid.live/
- **Color Scripter:** https://colorscripter.com/ (네이버용 코드 하이라이팅)
- **네이버 블로그:** https://blog.naver.com/

## 자주 묻는 질문

**Q: 다른 블로그 플랫폼에서도 사용할 수 있나요?**
A: 네이버 블로그에 최적화되어 있지만, 비슷한 제약이 있는 다른 플랫폼에서도 작동할 수 있습니다.

**Q: 왜 마크다운 미리보기에서 복사-붙여넣기가 안 되나요?**
A: 미리보기는 Mermaid 다이어그램을 올바르게 보존하지 못하고, 네이버 에디터가 클립보드 내용을 손상시킵니다.

**Q: mmdc가 필요한가요?**
A: 선택사항입니다. 없으면 mermaid.live에서 수동으로 다이어그램을 렌더링할 수 있습니다 (여전히 빠름).

**Q: Color Scripter를 건너뛸 수 있나요?**
A: 네 - 코드 블록은 일반 텍스트로 표시되며, 많은 사용 사례에서 충분합니다.

**Q: 원본 마크다운을 수정하나요?**
A: 아니오 - 변환기는 마크다운을 읽기만 합니다. 출력은 별도 디렉토리로 갑니다.

## 지원

도움이 필요하신가요?
1. `INSTRUCTIONS.md` (변환 후 생성) 업로드 단계 확인
2. 이 README 사용 정보 확인
3. GitHub Issues에 문제 제기

---

**즐거운 블로깅 되세요! 🚀**

Made with ❤️ for Korean bloggers
