# desktop_app.py - 完整的桌面版养老规划助手
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
from datetime import datetime

class PensionAdvisorDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("智能养老规划助手 - 专业版")
        self.root.geometry("800x900")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
        
    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                              text="🤖 智能养老规划助手", 
                              font=("微软雅黑", 18, "bold"),
                              fg="#2c3e50",
                              bg='#f0f0f0')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="专业养老规划 · 个性化资产配置",
                                 font=("微软雅黑", 10),
                                 fg="#7f8c8d",
                                 bg='#f0f0f0')
        subtitle_label.pack(pady=(5, 0))
        
        # 创建笔记本（选项卡）
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 信息输入选项卡
        self.input_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.input_frame, text="📝 基本信息")
        
        # 结果展示选项卡
        self.result_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.result_frame, text="📊 规划结果")
        
        self.setup_input_tab()
        self.setup_result_tab()
        
    def setup_input_tab(self):
        # 基本信息输入
        basic_frame = ttk.LabelFrame(self.input_frame, text="个人信息", padding="15")
        basic_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 第一行
        row1 = ttk.Frame(basic_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="年龄:").pack(side=tk.LEFT, padx=(0, 10))
        self.age_var = tk.StringVar(value="30")
        ttk.Entry(row1, textvariable=self.age_var, width=10).pack(side=tk.LEFT)
        
        ttk.Label(row1, text="年收入(元):").pack(side=tk.LEFT, padx=(20, 10))
        self.income_var = tk.StringVar(value="100000")
        ttk.Entry(row1, textvariable=self.income_var, width=15).pack(side=tk.LEFT)
        
        # 第二行
        row2 = ttk.Frame(basic_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="现有资产(元):").pack(side=tk.LEFT, padx=(0, 10))
        self.assets_var = tk.StringVar(value="50000")
        ttk.Entry(row2, textvariable=self.assets_var, width=15).pack(side=tk.LEFT)
        
        ttk.Label(row2, text="月支出(元):").pack(side=tk.LEFT, padx=(20, 10))
        self.expenses_var = tk.StringVar(value="5000")
        ttk.Entry(row2, textvariable=self.expenses_var, width=15).pack(side=tk.LEFT)
        
        # 第三行
        row3 = ttk.Frame(basic_frame)
        row3.pack(fill=tk.X, pady=5)
        
        ttk.Label(row3, text="计划退休年龄:").pack(side=tk.LEFT, padx=(0, 10))
        self.retirement_var = tk.StringVar(value="60")
        ttk.Entry(row3, textvariable=self.retirement_var, width=10).pack(side=tk.LEFT)
        
        # 风险评估
        risk_frame = ttk.LabelFrame(self.input_frame, text="风险评估", padding="15")
        risk_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 问题1
        ttk.Label(risk_frame, text="1. 您投资的主要目标是？", font=("微软雅黑", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.risk_q1 = tk.StringVar(value="B")
        ttk.Radiobutton(risk_frame, text="A) 资产保值，跑赢通胀就好", variable=self.risk_q1, value="A").pack(anchor=tk.W)
        ttk.Radiobutton(risk_frame, text="B) 资产稳健增长，愿意承担一定波动", variable=self.risk_q1, value="B").pack(anchor=tk.W)
        ttk.Radiobutton(risk_frame, text="C) 追求资产大幅增长，能接受短期较大亏损", variable=self.risk_q1, value="C").pack(anchor=tk.W)
        
        # 问题2
        ttk.Label(risk_frame, text="\n2. 您能接受的最大投资亏损是？", font=("微软雅黑", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.risk_q2 = tk.StringVar(value="B")
        ttk.Radiobutton(risk_frame, text="A) 5%以内", variable=self.risk_q2, value="A").pack(anchor=tk.W)
        ttk.Radiobutton(risk_frame, text="B) 5%-15%", variable=self.risk_q2, value="B").pack(anchor=tk.W)
        ttk.Radiobutton(risk_frame, text="C) 15%以上", variable=self.risk_q2, value="C").pack(anchor=tk.W)
        
        # 问题3
        ttk.Label(risk_frame, text="\n3. 您的投资经验如何？", font=("微软雅黑", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.risk_q3 = tk.StringVar(value="B")
        ttk.Radiobutton(risk_frame, text="A) 新手，刚开始学习投资", variable=self.risk_q3, value="A").pack(anchor=tk.W)
        ttk.Radiobutton(risk_frame, text="B) 有一些经验，投资过基金/股票", variable=self.risk_q3, value="B").pack(anchor=tk.W)
        ttk.Radiobutton(risk_frame, text="C) 经验丰富，经常进行投资操作", variable=self.risk_q3, value="C").pack(anchor=tk.W)
        
        # 生成按钮
        button_frame = ttk.Frame(self.input_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, 
                  text="🚀 生成养老规划", 
                  command=self.generate_plan,
                  style="Accent.TButton").pack(pady=10)
        
        # 配置强调按钮样式
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#3498db")
        
    def setup_result_tab(self):
        # 结果展示区域
        self.result_text = scrolledtext.ScrolledText(self.result_frame, 
                                                   wrap=tk.WORD, 
                                                   font=("Consolas", 10),
                                                   width=80, 
                                                   height=30)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 初始提示
        self.result_text.insert(tk.END, "请填写左侧信息并点击'生成养老规划'按钮...")
        self.result_text.config(state=tk.DISABLED)
    
    def calculate_risk_profile(self):
        """计算风险偏好"""
        score = 0
        answers = [self.risk_q1.get(), self.risk_q2.get(), self.risk_q3.get()]
        
        for answer in answers:
            if answer == 'A':
                score += 1
            elif answer == 'B':
                score += 2
            elif answer == 'C':
                score += 3
        
        age = int(self.age_var.get())
        
        # 年龄调整
        age_factor = max(0, (40 - age) / 20)
        adjusted_score = score * (1 + age_factor * 0.3)
        
        if adjusted_score <= 3.5:
            return "保守型", adjusted_score
        elif adjusted_score <= 6.5:
            return "稳健型", adjusted_score
        else:
            return "进取型", adjusted_score
    
    def calculate_retirement_needs(self):
        """计算养老资金需求"""
        age = int(self.age_var.get())
        retirement_age = int(self.retirement_var.get())
        monthly_expenses = int(self.expenses_var.get())
        
        years_to_retire = retirement_age - age
        annual_expenses = monthly_expenses * 12
        
        # 考虑通胀的养老资金估算
        inflation_rate = 1.03  # 3%年化通胀
        retirement_years = 25  # 假设退休后生活25年
        
        future_annual_expenses = annual_expenses * (inflation_rate ** years_to_retire)
        total_needed = future_annual_expenses * retirement_years
        monthly_savings = total_needed / (years_to_retire * 12)
        
        return {
            "years_to_retire": years_to_retire,
            "annual_expenses": annual_expenses,
            "total_retirement_needed": int(total_needed),
            "monthly_savings_needed": int(monthly_savings)
        }
    
    def generate_portfolio_allocation(self, risk_type):
        """生成投资组合配置"""
        age = int(self.age_var.get())
        assets = int(self.assets_var.get())
        
        if risk_type == "保守型":
            if age < 35:
                allocation = {"股票": 20, "债券": 50, "现金": 25, "另类投资": 5}
            elif age < 50:
                allocation = {"股票": 15, "债券": 55, "现金": 25, "另类投资": 5}
            else:
                allocation = {"股票": 10, "债券": 60, "现金": 25, "另类投资": 5}
                
        elif risk_type == "稳健型":
            if age < 35:
                allocation = {"股票": 50, "债券": 35, "现金": 10, "另类投资": 5}
            elif age < 50:
                allocation = {"股票": 40, "债券": 40, "现金": 15, "另类投资": 5}
            else:
                allocation = {"股票": 30, "债券": 45, "现金": 20, "另类投资": 5}
                
        else:  # 进取型
            if age < 35:
                allocation = {"股票": 70, "债券": 20, "现金": 5, "另类投资": 5}
            elif age < 50:
                allocation = {"股票": 60, "债券": 25, "现金": 10, "另类投资": 5}
            else:
                allocation = {"股票": 50, "债券": 30, "现金": 15, "另类投资": 5}
        
        # 资产规模调整
        if assets > 500000:
            allocation["另类投资"] += 5
            allocation["股票"] -= 3
            allocation["债券"] -= 2
        
        return allocation
    
    def get_product_recommendations(self, allocation):
        """获取产品推荐"""
        product_database = {
            "股票": ["沪深300指数基金", "中证500指数基金", "科技行业基金", "消费行业基金"],
            "债券": ["国债", "地方政府债基金", "高等级企业债基金", "可转债基金"],
            "现金": ["货币市场基金", "银行理财产品", "短期定期存款"],
            "另类投资": ["黄金ETF", "REITs基金", "大宗商品基金"]
        }
        
        recommendations = {}
        for category, percentage in allocation.items():
            if percentage > 0 and category in product_database:
                products = product_database[category]
                num_products = min(len(products), max(1, percentage // 20))
                recommendations[category] = {
                    "percentage": percentage,
                    "products": products[:num_products]
                }
        
        return recommendations
    
    def generate_plan(self):
        """生成完整的养老规划"""
        try:
            # 验证输入
            age = int(self.age_var.get())
            retirement_age = int(self.retirement_var.get())
            
            if retirement_age <= age:
                messagebox.showerror("输入错误", "退休年龄必须大于当前年龄")
                return
            
            # 计算各项数据
            risk_type, risk_score = self.calculate_risk_profile()
            retirement_data = self.calculate_retirement_needs()
            allocation = self.generate_portfolio_allocation(risk_type)
            product_recommendations = self.get_product_recommendations(allocation)
            
            # 生成报告
            report = self.generate_report(risk_type, retirement_data, allocation, product_recommendations)
            
            # 显示结果
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, report)
            self.result_text.config(state=tk.DISABLED)
            
            # 切换到结果选项卡
            self.notebook.select(1)
            
        except ValueError as e:
            messagebox.showerror("输入错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"生成规划时出错: {str(e)}")
    
    def generate_report(self, risk_type, retirement_data, allocation, product_recommendations):
        """生成格式化报告"""
        report = f"""
{'='*70}
📊 个性化养老规划综合报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

👤 客户档案
{'─'*70}
   年龄: {self.age_var.get()}岁
   年收入: {int(self.income_var.get()):,}元
   现有资产: {int(self.assets_var.get()):,}元
   月支出: {int(self.expenses_var.get()):,}元
   计划退休: {self.retirement_var.get()}岁
   风险偏好: {risk_type}

💰 养老需求分析
{'─'*70}
   距离退休: {retirement_data['years_to_retire']}年
   当前年支出: {retirement_data['annual_expenses']:,}元
   预计养老资金需求: {retirement_data['total_retirement_needed']:,}元
   建议月储蓄额: {retirement_data['monthly_savings_needed']:,}元

🎯 投资配置建议
{'─'*70}
"""
        
        # 添加配置详情
        total_percentage = 0
        for category, percentage in allocation.items():
            if percentage > 0:
                report += f"   {category}: {percentage}%\n"
                total_percentage += percentage
        
        report += f"   总计: {total_percentage}%\n\n"
        
        # 产品推荐
        report += "📈 具体产品推荐\n"
        report += "─"*70 + "\n"
        for category, info in product_recommendations.items():
            report += f"\n   {category} ({info['percentage']}%):\n"
            for product in info['products']:
                report += f"      • {product}\n"
        
        # 行动计划
        report += f"""
💡 行动计划
{'─'*70}
   1. 立即开始每月储蓄 {retirement_data['monthly_savings_needed']:,}元
   2. 按照上述比例配置现有资产
   3. 每半年回顾调整投资组合
   4. 随着年龄增长逐步降低风险暴露

📝 实施建议
{'─'*70}
   • 建立专门的养老储蓄账户
   • 设置每月自动转账
   • 定期学习理财知识
   • 保持长期投资心态

⚠️ 风险提示
{'─'*70}
   1. 本建议基于提供信息生成，仅供参考
   2. 投资有风险，过往业绩不代表未来表现
   3. 市场波动可能导致短期亏损
   4. 建议咨询专业理财顾问完善规划

{'='*70}
"""
        return report

def main():
    root = tk.Tk()
    app = PensionAdvisorDesktop(root)
    root.mainloop()

if __name__ == "__main__":
    main()