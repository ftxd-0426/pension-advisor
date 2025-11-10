# pension_advisor_improved.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import sys
import json
from datetime import datetime
import os

print("=" * 60)
print("🤖 智能养老规划助手 - 专业版")
print("=" * 60)
print("正在初始化 deepseek-r1:1.5b 模型...")

class InvestmentAdviceParser(BaseOutputParser):
    """解析AI的投资建议"""
    def parse(self, text: str):
        # 简单的解析，提取关键信息
        return {
            "raw_advice": text,
            "contains_risk_warning": "风险" in text or "谨慎" in text,
            "contains_growth_advice": "增长" in text or "收益" in text
        }

class ImprovedPensionAdvisor:
    def __init__(self):
        try:
            # 使用新的 OllamaLLM 替代弃用的 Ollama
            self.llm = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.3)
            self.model_loaded = True
            print("✅ deepseek-r1:1.5b 模型加载成功！")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            self.model_loaded = False
            return
        
        # 更专业的对话流程
        self.conversation_stages = {
            "welcome": "您好！我是您的专业养老规划助手。我将通过几个关键问题为您制定个性化的养老规划方案。",
            "age": "请问您的年龄是？",
            "income": "感谢告知！请问您的年收入大概是多少呢？（包括工资、奖金等所有收入）",
            "assets": "了解！请问您目前已有的可用于投资的资产总额大概是？（包括存款、基金、股票等）",
            "expenses": "为了更好地规划，请问您每月的必要生活开支大约是多少？",
            "retirement_age": "您计划在多少岁退休？",
            "risk_q1": "接下来评估您的风险偏好：\n问题1：您投资的主要目标是？\nA) 资产保值，跑赢通胀就好\nB) 资产稳健增长，愿意承担一定波动\nC) 追求资产大幅增长，能接受短期较大亏损",
            "risk_q2": "问题2：您能接受的最大投资亏损是？\nA) 5%以内\nB) 5%-15%\nC) 15%以上",
            "risk_q3": "问题3：您的投资经验如何？\nA) 新手，刚开始学习投资\nB) 有一些经验，投资过基金/股票\nC) 经验丰富，经常进行投资操作",
            "additional_goals": "除了养老规划，您还有其他重要的财务目标吗？（如购房、子女教育、旅游等）"
        }
        
        # 存储用户信息
        self.user_profile = {}
        self.current_stage = "welcome"
        self.stages_order = list(self.conversation_stages.keys())
        self.current_stage_index = 0
        
        # 投资产品数据库（简化版）
        self.investment_products = {
            "股票类": ["指数基金(如沪深300)", "行业基金(如科技、消费)", "蓝筹股", "成长股"],
            "债券类": ["国债", "企业债基金", "可转债基金", "债券ETF"],
            "现金类": ["货币基金", "银行理财", "定期存款", "活期存款"],
            "另类投资": ["黄金ETF", "REITs(房地产信托)", "大宗商品基金"]
        }
        
        self.parser = InvestmentAdviceParser()
        
    def start_conversation(self):
        if not self.model_loaded:
            return
            
        print(f"\n小智: {self.conversation_stages[self.current_stage]}")
        
    def calculate_retirement_needs(self):
        """计算养老资金需求"""
        try:
            age = int(self.user_profile.get('age', 30))
            retirement_age = int(self.user_profile.get('retirement_age', 60))
            monthly_expenses = int(self.user_profile.get('expenses', 5000))
            annual_expenses = monthly_expenses * 12
            
            # 简单估算：假设退休后生活25年，年化通胀3%
            retirement_years = 25
            inflation_adjustment = 1.03 ** (retirement_age - age)
            total_needed = annual_expenses * retirement_years * inflation_adjustment
            
            return {
                "retirement_age": retirement_age,
                "years_to_retire": retirement_age - age,
                "annual_expenses": annual_expenses,
                "total_retirement_needed": int(total_needed),
                "monthly_savings_needed": int(total_needed / ((retirement_age - age) * 12))
            }
        except:
            return None
    
    def calculate_risk_profile(self):
        """更精确的风险评估"""
        score = 0
        for i in range(1, 4):
            answer = self.user_profile.get(f'risk_q{i}', '').upper()
            if answer == 'A':
                score += 1
            elif answer == 'B':
                score += 2
            elif answer == 'C':
                score += 3
        
        age = int(self.user_profile.get('age', 30))
        
        # 年龄调整：年轻人可以承担更多风险
        age_factor = max(0, (40 - age) / 20)  # 40岁以下有额外风险承受加成
        
        adjusted_score = score * (1 + age_factor * 0.3)
        
        if adjusted_score <= 3.5:
            return "保守型", adjusted_score
        elif adjusted_score <= 6.5:
            return "稳健型", adjusted_score
        else:
            return "进取型", adjusted_score
    
    def generate_portfolio_allocation(self):
        """生成更精细的投资组合"""
        risk_type, score = self.calculate_risk_profile()
        age = int(self.user_profile['age'])
        assets = int(self.user_profile.get('assets', 0))
        
        # 更复杂的配置逻辑
        if risk_type == "保守型":
            if age < 35:
                base_allocation = {"股票": 20, "债券": 50, "现金": 25, "另类": 5}
            elif age < 50:
                base_allocation = {"股票": 15, "债券": 55, "现金": 25, "另类": 5}
            else:
                base_allocation = {"股票": 10, "债券": 60, "现金": 25, "另类": 5}
                
        elif risk_type == "稳健型":
            if age < 35:
                base_allocation = {"股票": 50, "债券": 35, "现金": 10, "另类": 5}
            elif age < 50:
                base_allocation = {"股票": 40, "债券": 40, "现金": 15, "另类": 5}
            else:
                base_allocation = {"股票": 30, "债券": 45, "现金": 20, "另类": 5}
                
        else:  # 进取型
            if age < 35:
                base_allocation = {"股票": 70, "债券": 20, "现金": 5, "另类": 5}
            elif age < 50:
                base_allocation = {"股票": 60, "债券": 25, "现金": 10, "另类": 5}
            else:
                base_allocation = {"股票": 50, "债券": 30, "现金": 15, "另类": 5}
        
        # 根据资产规模微调
        if assets > 500000:  # 资产较多时增加分散化
            base_allocation["另类"] += 5
            base_allocation["股票"] -= 3
            base_allocation["债券"] -= 2
        
        return base_allocation, risk_type
    
    def get_product_recommendations(self, allocation):
        """根据配置比例推荐具体产品"""
        recommendations = {}
        for category, percentage in allocation.items():
            if percentage > 0:
                products = self.investment_products.get(category, [])
                # 根据百分比决定推荐产品数量
                num_products = min(len(products), max(1, percentage // 20))
                recommendations[category] = {
                    "percentage": percentage,
                    "products": products[:num_products]
                }
        return recommendations
    
    def generate_ai_advice(self, allocation, risk_type, retirement_data):
        """使用AI生成个性化建议"""
        try:
            prompt = f"""
用户档案：
- 年龄: {self.user_profile['age']}岁
- 年收入: {self.user_profile['income']}元
- 现有资产: {self.user_profile['assets']}元
- 月支出: {self.user_profile.get('expenses', '未知')}元
- 计划退休年龄: {self.user_profile.get('retirement_age', 60)}岁
- 风险偏好: {risk_type}

养老需求分析：
- 距离退休: {retirement_data['years_to_retire']}年
- 预计所需养老资金: {retirement_data['total_retirement_needed']:,}元
- 建议每月储蓄: {retirement_data['monthly_savings_needed']:,}元

投资配置：
{allocation}

请用专业但易懂的中文给出：
1. 对这个配置的简要评价
2. 针对该用户的2-3条具体建议
3. 重要的风险提示

请保持回答简洁明了，不超过200字。
"""
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            return f"AI建议生成遇到技术问题: {str(e)}"
    
    def generate_comprehensive_report(self):
        """生成完整的养老规划报告"""
        # 计算各项数据
        allocation, risk_type = self.generate_portfolio_allocation()
        retirement_data = self.calculate_retirement_needs()
        product_recommendations = self.get_product_recommendations(allocation)
        ai_advice = self.generate_ai_advice(allocation, risk_type, retirement_data)
        
        # 生成报告
        report = f"""
{'='*70}
📊 个性化养老规划综合报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*70}

👤 客户档案
{'─'*70}
   ▪ 年龄: {self.user_profile['age']}岁
   ▪ 年收入: {self.user_profile['income']:,}元
   ▪ 现有资产: {self.user_profile['assets']:,}元
   ▪ 月支出: {self.user_profile.get('expenses', '未提供')}元
   ▪ 计划退休: {self.user_profile.get('retirement_age', 60)}岁
   ▪ 风险偏好: {risk_type}

💰 养老需求分析
{'─'*70}
   ▪ 距离退休: {retirement_data['years_to_retire']}年
   ▪ 预计养老资金需求: {retirement_data['total_retirement_needed']:,}元
   ▪ 建议月储蓄额: {retirement_data['monthly_savings_needed']:,}元

🎯 投资配置建议
{'─'*70}
"""
        
        # 添加配置详情
        for category, info in product_recommendations.items():
            report += f"   ▪ {category}: {info['percentage']}%\n"
            for product in info['products']:
                report += f"      - {product}\n"
        
        report += f"""
💡 专业建议
{'─'*70}
   {ai_advice}

📈 行动计划
{'─'*70}
   1. 立即开始每月储蓄 {retirement_data['monthly_savings_needed']:,}元
   2. 按照上述比例配置现有资产
   3. 每半年回顾调整投资组合
   4. 随着年龄增长逐步降低风险

⚠️ 风险提示
{'─'*70}
   1. 本建议基于提供信息生成，仅供参考
   2. 投资有风险，过往业绩不代表未来表现
   3. 建议咨询专业理财顾问完善规划
   4. 市场波动可能导致短期亏损

{'='*70}
"""
        return report
    
    def process_user_input(self, user_input):
        if not self.model_loaded:
            return "模型未正确加载，无法继续对话。", True
        
        # 存储用户回答
        current_stage_key = self.stages_order[self.current_stage_index]
        self.user_profile[current_stage_key] = user_input
        
        # 移动到下一阶段
        self.current_stage_index += 1
        
        # 检查是否所有阶段都已完成
        if self.current_stage_index >= len(self.stages_order):
            report = self.generate_comprehensive_report()
            return report, True
        else:
            next_stage_key = self.stages_order[self.current_stage_index]
            next_question = self.conversation_stages[next_stage_key]
            return f"小智: {next_question}", False

def main():
    # 检查是否需要安装新包
    try:
        from langchain_ollama import OllamaLLM
    except ImportError:
        print("❌ 需要安装 langchain-ollama 包")
        print("请运行: pip install langchain-ollama")
        input("按回车键退出...")
        return
    
    advisor = ImprovedPensionAdvisor()
    
    if not advisor.model_loaded:
        print("❌ 无法启动助手")
        input("按回车键退出...")
        return
        
    advisor.start_conversation()
    
    print("\n💡 提示: 您可以随时输入'退出'来结束对话。")
    print("💡 提示: 输入'跳过'可以跳过当前问题。\n")
    
    while True:
        try:
            user_input = input("您: ").strip()
            
            if user_input.lower() in ['退出', 'quit', 'exit', '结束']:
                print("\n小智: 感谢使用专业养老规划助手！再见！")
                break
                
            if user_input.lower() in ['跳过', 'skip']:
                user_input = "未提供"
                
            if not user_input:
                print("小智: 抱歉，我没有收到您的输入，请再说一遍~")
                continue
                
            # 处理用户输入
            response, should_exit = advisor.process_user_input(user_input)
            print(f"\n{response}")
            
            # 检查是否应该退出
            if should_exit:
                print("\n🎉 报告生成完成！感谢您的使用。")
                break
                
        except KeyboardInterrupt:
            print("\n\n感谢使用！再见！")
            break
        except Exception as e:
            print(f"\n小智: 抱歉，出现了一些问题: {e}")

if __name__ == "__main__":
    main()