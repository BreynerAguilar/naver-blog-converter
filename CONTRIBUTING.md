# 기여 가이드 (Contributing Guide)

네이버 블로그 변환기에 기여해주셔서 감사합니다!

Thank you for contributing to Naver Blog Converter!

## 한국어

### 이슈 제보

버그나 기능 요청이 있으시면:
1. [Issues](https://github.com/YOUR_USERNAME/naver-blog-converter/issues)에서 기존 이슈 확인
2. 없으면 새 이슈 생성
3. 가능한 자세히 설명 (재현 방법, 환경 등)

### 풀 리퀘스트

1. 저장소 포크
2. 기능 브랜치 생성: `git checkout -b feature/amazing-feature`
3. 변경사항 커밋: `git commit -m 'Add amazing feature'`
4. 브랜치에 푸시: `git push origin feature/amazing-feature`
5. Pull Request 열기

### 코드 스타일

- Python 3.11+ 타입 힌트 사용
- 함수는 단일 목적으로 작성
- 긴 작업에는 진행 상황 출력
- 수동 단계에 대한 도움말 제공

### 테스트

변경 후 테스트:
```bash
# 기본 변환 테스트
uv run python md2naver.py test-file.md

# GCS 업로드 테스트
uv run python md2naver.py test-file.md --gcs
```

## English

### Reporting Issues

If you find a bug or want to request a feature:
1. Check existing [Issues](https://github.com/YOUR_USERNAME/naver-blog-converter/issues)
2. Create a new issue if not found
3. Provide details (reproduction steps, environment, etc.)

### Pull Requests

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Style

- Use Python 3.11+ type hints
- Keep functions focused and single-purpose
- Print progress updates for long operations
- Provide helpful instructions for manual steps

### Testing

Test after changes:
```bash
# Test basic conversion
uv run python md2naver.py test-file.md

# Test with GCS upload
uv run python md2naver.py test-file.md --gcs
```

## 라이선스 / License

By contributing, you agree that your contributions will be licensed under the MIT License.
