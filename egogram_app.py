import sys
import random
import datetime
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# 質問と自我状態のリスト
questions = [
    ("自分の意見を主張するより、相手に合わせます", "AC"),
    ("気楽なおしゃべりをします", "FC"),
    ("夢中になって、時間を忘れることがあります", "FC"),
    ("ルールを守らない相手には、守るように言います", "CP"),
    ("物事は冷静に、落ち着いて判断します", "A"),
    ("他人には、温かく接するようにしています", "NP"),
    ("自分の考えを述べるまでに時間がかかります", "AC"),
    ("人を厳しく指導することがあります", "CP"),
    ("相手の気持ちに、寄り添うようにしています", "NP"),
    ("予定や計画などの時間管理を、記録しています", "A"),
    ("相手の嫌な言葉を、黙って聞くことがあります", "AC"),
    ("計画は、必要に応じて見直しながら実行します", "A"),
    ("うれしいときは、声に出して喜びます", "FC"),
    ("人から相談されたら、親身になって耳を傾けます", "NP"),
    ("公私のケジメをつけて行動します", "CP"),
    ("相手の成長のためには、欠点も指摘します", "CP"),
    ("周囲に配慮し、気持ちをおさえることがあります", "AC"),
    ("人に気を遣うより、自由に行動します", "FC"),
    ("現実を十分調べた上で行動します", "A"),
    ("人の世話をするのが好きです", "NP"),
    ("自己主張の強い人には、何も言えなくなります", "AC"),
    ("相手のために厳正な判断をします", "CP"),
    ("賛否両論を公平に聞いて、結論を出します", "A"),
    ("相手の些細な間違いも、見逃しません", "CP"),
    ("いろいろなことに、好奇心が沸きます", "FC"),
    ("情報はデータや根拠を調べるようにしています", "A"),
    ("人が困っているときには、手を差しのべます", "NP"),
    ("人の良いところは、正しく評価すべきです", "CP"),
    ("人を避けることがあります", "AC"),
    ("人の長所を見つけて、ほめます", "NP"),
    ("人の意見が事実に基づいているか、考えます", "A"),
    ("自分が興味をもったものに、相手を誘います", "FC"),
    ("人への思いやりを行動で示します", "NP"),
    ("相手のまちがいに気づいたときは、指摘します", "CP"),
    ("「ありがとう」などの感謝の言葉が自然に出ます", "NP"),
    ("判断や行動の前に、情報収集を行うようにしています", "A"),
    ("自分が悪いときは、素直にあやまります", "AC"),
    ("数字を話題にするとき、確かめて使います", "A"),
    ("相手の一言が気にかかることがあります", "AC"),
    ("自分の言動を振り返り、よく後悔します", "AC"),
    ("楽しいかどうかで、するかしないかを決めることがあります", "FC"),
    ("人の道に外れたことは、許しません", "CP"),
    ("心がワクワクするような趣味を、もっています", "FC"),
    ("相手の良い面を見るようにしています", "NP"),
    ("情報は、ポイントをまとめて伝えます", "A"),
    ("自分が正しいと思ったことは、曲げません", "CP"),
    ("人の心を穏やかにするように、接しています", "NP"),
    ("明るく、活き活きと生活しています", "FC"),
    ("相手の機嫌が良いか悪いか、気になります", "AC"),
    ("自分の気持ちに従って、自然に振る舞います", "FC")
]

# 回答の選択肢とスコア
answers = {
    "いつもする": 2,
    "ときどきする": 1,
    "ほとんどしない": 0
}

# 自我状態の初期スコア
ego_states = {
    "CP": 0,
    "NP": 0,
    "A": 0,
    "FC": 0,
    "AC": 0
}

class MainWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle('EGOGRAM')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        layout = QVBoxLayout()
        self.setLayout(layout)

        start_button = QPushButton('測定開始', self)
        start_button.clicked.connect(self.start_measurement)
        layout.addWidget(start_button)

    def start_measurement(self):
        self.stacked_widget.setCurrentIndex(1)

class QuestionWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_question = 0
        self.scores = ego_states.copy()
        self.answers = []  # 選択した回答を保存するリストを追加
        random.shuffle(questions)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('EGOGRAM')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.question_label = QLabel(self)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.question_label)

        self.answer_layout = QHBoxLayout()
        self.layout.addLayout(self.answer_layout)

        self.answer_buttons = []
        for answer in answers.keys():
            btn = QPushButton(answer, self)
            btn.clicked.connect(self.record_answer)
            self.answer_buttons.append(btn)
            self.answer_layout.addWidget(btn)

        self.show_question()

    def show_question(self):
        if self.current_question < len(questions):
            question, _ = questions[self.current_question]
            self.question_label.setText(f"質問 {self.current_question + 1}: {question}")
        else:
            self.stacked_widget.setCurrentIndex(2)
            self.stacked_widget.widget(2).display_scores(self.scores)

    def record_answer(self):
        sender = self.sender()
        answer = sender.text()
        _, ego_state = questions[self.current_question]
        self.scores[ego_state] += answers[answer]
        self.answers.append(answer)  # 選択した回答を保存
        self.current_question += 1
        self.show_question()

class ResultWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # stacked_widgetを保存
        self.initUI()

    def initUI(self):
        self.setWindowTitle('EGOGRAM')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.score_labels = {}
        for state in ego_states.keys():
            label = QLabel(self)
            self.layout.addWidget(label)
            self.score_labels[state] = label

        self.plot_button = QPushButton('グラフを表示', self)
        self.plot_button.clicked.connect(self.plot_egogram)
        self.layout.addWidget(self.plot_button)

        self.save_button = QPushButton('PDFに保存', self)
        self.save_button.clicked.connect(self.save_pdf)
        self.layout.addWidget(self.save_button)

        # 終了ボタンを追加
        self.exit_button = QPushButton('終了', self)
        self.exit_button.clicked.connect(self.exit_application)
        self.layout.addWidget(self.exit_button)

    def display_scores(self, scores):
        for state, score in scores.items():
            self.score_labels[state].setText(f"{state}: {score}")

    def plot_egogram(self, save_only=False):
        # エゴグラムをプロット
        states = list(self.score_labels.keys())
        scores = [int(label.text().split(": ")[1]) for label in self.score_labels.values()]
        plt.figure(figsize=(10, 6))
        plt.plot(states, scores, marker='o')
        plt.title(f"Your Egogram ({datetime.datetime.now().strftime('%Y/%m/%d')})")
        plt.ylim(0, 20)
        plt.yticks(range(0, 21, 5))
        plt.grid(True)
        
        # Add data labels
        for i, score in enumerate(scores):
            plt.text(i, -1, f'{score}', ha='center', va='top', fontsize=12) # スコアを項目の下に表示
        
        plt.savefig('egogram.png')
        
        if not save_only:
            plt.show()

    def save_pdf(self):
        # グラフが保存されていなければプロットして保存
        if not os.path.exists('egogram.png'):
            self.plot_egogram(save_only=True)
        
        # PDFに結果を保存
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.add_font('IPAexG', '', 'ipaexg.ttf', uni=True)  # 日本語フォントを追加
        pdf.set_font('IPAexG', '', 12)
        pdf.image('egogram.png', x=10, y=20, w=270)
        
        # 2ページ目を追加
        pdf.add_page()
        pdf.set_font('IPAexG', '', 12)
        
        # 質問と自我状態、選択した回答の一覧を追加
        pdf.cell(0, 10, '質問と自我状態、選択した回答の一覧', ln=True)
        for i, (question, ego_state) in enumerate(questions):
            answer = self.stacked_widget.widget(1).answers[i]  # 選択した回答を取得
            pdf.cell(0, 10, f'質問 {i+1}: {question} - 自我状態: {ego_state} - 回答: {answer}', ln=True)
        
        pdf.output("egogram.pdf")
        QMessageBox.information(self, "完了", "結果がPDFとして保存されました。")

    def exit_application(self):
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    main_window = MainWindow(stacked_widget)
    question_window = QuestionWindow(stacked_widget)
    result_window = ResultWindow(stacked_widget)  # stacked_widgetを渡す

    stacked_widget.addWidget(main_window)
    stacked_widget.addWidget(question_window)
    stacked_widget.addWidget(result_window)

    stacked_widget.setCurrentIndex(0)

    stacked_widget.show()
    app.exec_()  # ここでアプリケーションのイベントループを開始します