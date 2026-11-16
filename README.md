# Japanese Anime Subtitles

Nơi lưu phụ đề tiếng Nhật để học anime bằng [asbplayer](https://docs.asbplayer.dev/).

## Chi's Sweet Home (2008)

- [Tập 001–010](subtitles/chis-sweet-home): 10 file phụ đề Nhật dạng SRT, mỗi tập một file.
- Tên file: `001.ja.srt` ... `010.ja.srt`.
- Nguồn chuyển đổi: nhóm **Kamigami**, file `[Kamigami][Chi’s Sweet Home][01-16][JPN].ass`, được lưu tại [Kitsunekko mirror](https://github.com/Ajatt-Tools/kitsunekko-mirror/tree/main/subtitles/anime_tv).
- Chỉ giữ các dòng phụ đề tiếng Nhật; mốc thời gian đã đặt lại cho từng tập.
- **Chưa kiểm tra đồng bộ với video AnimeVietSub**. Có thể cần chỉnh subtitle offset trong asbplayer.

> Repo hiện là **Public**. Nếu dùng để lưu cá nhân, nên chuyển sang **Private** trong GitHub Settings → General → Danger Zone. Hãy xác minh quyền tái phân phối trước khi chia sẻ hoặc tải lên Jimaku.

## Cách dùng

Mở video tương ứng, vào asbplayer → Load Subtitles → chọn file `.ja.srt`. Nếu phụ đề xuất hiện lệch lời thoại, chỉnh subtitle offset.


## Tra cứu từ vựng trên web

Trang tra cứu nằm trong `docs/index.html` và sử dụng `docs/subtitles-index.json`.
Hiện đã lập chỉ mục **407 câu từ tập 001–010**.

**Bật GitHub Pages lần đầu:** Repository → **Settings → Pages** → **Build and deployment** → Source **Deploy from a branch** → Branch **main**, folder **/docs** → **Save**.

Sau khi GitHub Pages xuất bản xong, mở:

**https://dankhoi24.github.io/japanese-anime-subtitle-toolkit/**

Tính năng: tìm từ/cụm từ Nhật theo nội dung phụ đề, lọc theo tập, xem câu và timestamp, copy thời gian, mở video. URL trực tiếp được xác minh mới có tập 001; khi tìm tập khác, có thể tự **Gắn link tập** một lần trên trình duyệt hoặc mở trang danh sách tập. Liên kết riêng được lưu bằng localStorage của trình duyệt đó.

**Giới hạn:** Mở video không tự tua chính xác đến timestamp vì chưa xác nhận AnimeVietSub hỗ trợ deep link theo thời gian. Nút mở video sẽ đồng thời sao chép mốc phút:giây, để bạn tua hoặc dùng asbplayer. Video và audio không được lưu trữ trên GitHub Pages.
