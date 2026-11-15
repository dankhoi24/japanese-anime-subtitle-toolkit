# Pipeline architecture

1. **Source:** Download combined Japanese Kamigami ASS, or use a locally cached copy in `sources/` (gitignored).
2. **Segment:** Detect the repeated Japanese opening line; fail if opening counts or gaps are unexpected.
3. **Extract:** Keep the Japanese dialogue styles, remove ASS formatting tags.
4. **Export:** Rebase episode timestamps and save separate UTF-8 SRTs under `output/chis-sweet-home/` (gitignored).
5. **Validate:** Check format and basic timestamp validity; this does not validate alignment with AnimeVietSub or spoken dialogue.
6. **Review:** Compare with video manually and adjust subtitle offset as needed.
7. **Distribute:** Do not publish subtitle text without checking redistribution rights. Jimaku upload is not automated.

The source groups in config cover episodes 001–104. The 001–016 source was inspected; later group structures require verification.

No Jimaku credentials, API tokens, or fan-made subtitle texts are committed.
