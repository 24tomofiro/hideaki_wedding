import re

html_content = """                 <!-- Message Card 1 -->
                <div class="message-card reveal" onclick="this.classList.toggle('expanded')">
                    <div class="message-summary">
                        <p class="message-text">"人生であと５回くらいしか会わないと思うけど、今後もよろしく！"</p>
                        <p class="message-author">- 早瀬友洋</p>
                        <span class="expand-hint">▼ tap to see profile</span>
                    </div>
                    <div class="friend-profile-content">
                        <table class="friend-details">
                            <tr><th>総評</th><td>コソコソ会ってる関係</td></tr>
                            <tr><th>友好度</th><td class="stars">★★★★★</td></tr>
                            <tr><th>最終連絡</th><td><span class="contact-date">2023.02.18</span><span class="contact-note">多分岩手でひでと遊んだであろうLINE</span></td></tr>
                        </table>
                    </div>
                </div>
"""

for i in range(2, 8):
    html_content += f"""
                <!-- Message Card {i} -->
                <div class="message-card reveal" style="transition-delay: 0.{i-1}s;" onclick="this.classList.toggle('expanded')">
                    <div class="message-summary">
                        <p class="message-text">"お祝いのメッセージ内容をここに入力してください。"</p>
                        <p class="message-author">- 友人 名前</p>
                        <span class="expand-hint">▼ tap to see profile</span>
                    </div>
                    <div class="friend-profile-content">
                        <table class="friend-details">
                            <tr><th>総評</th><td>ここに関係性を入力</td></tr>
                            <tr><th>友好度</th><td class="stars">★★★★☆</td></tr>
                            <tr><th>最終連絡</th><td><span class="contact-date">YYYY.MM.DD</span><span class="contact-note">連絡ログのメモ</span></td></tr>
                        </table>
                    </div>
                </div>
"""

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace everything from <div class="messages-grid"> to the end of the section
pattern = r'(<div class="messages-grid">)(.*?)(</section>)'
def replacer(match):
    return match.group(1) + '\n' + html_content + '            </div>\n        </div>\n    ' + match.group(3)

new_text = re.sub(pattern, replacer, text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Fixed HTML.")
