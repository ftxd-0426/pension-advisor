# advisor_core.py - 养老规划核心逻辑
from datetime import datetime

class PensionAdvisorCore:
    def __init__(self, use_ai=True):
        self.use_ai = use_ai
        # 注意：为了简化部署，我们默认不使用AI模型
        # 如果需要AI功能，可以在Zeabur上配置Ollama
    
    def calculate_retirement_needs(self, user_data):
        """计算养老资金需求"""
        try:
            age = int(user_data.get('age', 30))
            retirement_age = int(user_data.get('retirement_age', 60))
            monthly_expenses = int(user_data.get('monthly_expenses', 5000))
            annual_expenses = monthly_expenses * 12
            
            # 养老资金估算
            retirement_years = 25
            inflation_rate = 1.03
            years_to_retire = retirement_age - age
            
            future_annual_expenses = annual_expenses * (inflation_rate ** years_to_retire)
            total_needed = future_annual_expenses * retirement_years
            
            return {
                "years_to_retire": years_to_retire,
                "annual_expenses": annual_expenses,
                "total_retirement_needed": int(total_needed),
                "monthly_savings_needed": int(total_needed / (years_to_retire * 12))
            }
        except Exception as e:
            # 简化计算作为备选
            years_to_retire = retirement_age - age
            total_needed = monthly_expenses * 12 * 25
            return {
                "years_to_retire": years_to_retire,
                "annual_expenses": monthly_expenses * 12,
                "total_retirement_needed": total_needed,
                "monthly_savings_needed": total_needed // (years_to_retire * 12)
            }
    
    def calculate_risk_profile(self, user_data):
        """计算风险偏好"""
        score = 0
        for i in range(1, 4):
            answer = user_data.get(f'risk_q{i}', 'B').upper()
            if answer == 'A':
                score += 1
            elif answer == 'B':
                score += 2
            elif answer == 'C':
                score += 3
        
        age = int(user_data.get('age', 30))
        
        # 年龄调整
        age_factor = max(0, (40 - age) / 20)
        adjusted_score = score * (1 + age_factor * 0.3)
        
        if adjusted_score <= 3.5:
            return "保守型", adjusted_score
        elif adjusted_score <= 6.5:
            return "稳健型", adjusted_score
        else:
            return "进取型", adjusted_score
    
    def generate_portfolio_allocation(self, user_data):
        """生成投资组合配置"""
        risk_type, score = self.calculate_risk_profile(user_data)
        age = int(user_data['age'])
        assets = int(user_data.get('current_assets', 0))
        
        # 配置逻辑
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
        
        return allocation, risk_type
    
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
    
    def generate_ai_advice(self, user_data, allocation, risk_type, retirement_data):
        """生成AI建议"""
        # 简化的建议，不依赖AI模型
        age = user_data['age']
        
        if risk_type == "保守型":
            advice = f"基于您{age}岁的年龄和保守型风险偏好，此配置注重资金安全，适合风险承受能力较低的投资者。建议重点关注债券和现金类资产的稳定性。"
        elif risk_type == "稳健型":
            advice = f"作为{age}岁的投资者，此平衡型配置在追求收益的同时控制风险。建议定期调整保持股债平衡，长期坚持投资纪律。"
        else:
            advice = f"考虑到您{age}岁相对年轻且能承受较高风险，此进取型配置旨在追求长期增长。请注意市场波动风险，建议逐步积累投资经验。"
        
        advice += " 本建议基于标准理财规则生成，投资有风险，决策需谨慎。"
        return advice
    
    def generate_comprehensive_plan(self, user_data):
        """生成完整的养老规划"""
        # 计算各项数据
        allocation, risk_type = self.generate_portfolio_allocation(user_data)
        retirement_data = self.calculate_retirement_needs(user_data)
        product_recommendations = self.get_product_recommendations(allocation)
        ai_advice = self.generate_ai_advice(user_data, allocation, risk_type, retirement_data)
        
        # 组装完整结果
        result = {
            "user_profile": {
                "age": user_data['age'],
                "annual_income": user_data['annual_income'],
                "current_assets": user_data['current_assets'],
                "monthly_expenses": user_data['monthly_expenses'],
                "retirement_age": user_data['retirement_age'],
                "risk_profile": risk_type
            },
            "retirement_analysis": retirement_data,
            "portfolio_allocation": allocation,
            "product_recommendations": product_recommendations,
            "ai_advice": ai_advice,
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return result