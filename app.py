# app.py - Flask Web 应用
from flask import Flask, render_template, request, jsonify
from advisor_core import PensionAdvisorCore
import json
from datetime import datetime
import os
from flask import Flask, render_template, request, jsonify
# ... 其他导入

app = Flask(__name__)

# 初始化养老规划核心
advisor = PensionAdvisorCore()

@app.route('/')
def index():
    """显示主页面"""
    return render_template('../index.html')

@app.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "Pension Advisor API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/plan', methods=['POST'])
def generate_plan():
    """生成养老规划API"""
    try:
        # 获取用户数据
        user_data = request.get_json()
        
        # 验证必需字段
        required_fields = ['age', 'annual_income', 'current_assets', 'monthly_expenses', 'retirement_age']
        for field in required_fields:
            if field not in user_data:
                return jsonify({
                    "success": False,
                    "error": f"缺少必需字段: {field}"
                }), 400
        
        # 验证数字字段
        try:
            age = int(user_data['age'])
            annual_income = int(user_data['annual_income'])
            current_assets = int(user_data['current_assets'])
            monthly_expenses = int(user_data['monthly_expenses'])
            retirement_age = int(user_data['retirement_age'])
            
            if retirement_age <= age:
                return jsonify({
                    "success": False,
                    "error": "退休年龄必须大于当前年龄"
                }), 400
                
        except ValueError:
            return jsonify({
                "success": False,
                "error": "请输入有效的数字"
            }), 400
        
        # 准备完整用户数据
        full_user_data = {
            'age': age,
            'annual_income': annual_income,
            'current_assets': current_assets,
            'monthly_expenses': monthly_expenses,
            'retirement_age': retirement_age,
            'risk_q1': user_data.get('risk_q1', 'B'),
            'risk_q2': user_data.get('risk_q2', 'B'),
            'risk_q3': user_data.get('risk_q3', 'B')
        }
        
        # 生成规划
        plan_result = advisor.generate_comprehensive_plan(full_user_data)
        
        return jsonify({
            "success": True,
            "data": plan_result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"生成规划时出错: {str(e)}"
        }), 500

@app.route('/api/simple_plan', methods=['POST'])
def generate_simple_plan():
    """简化版规划生成（不依赖AI模型）"""
    try:
        user_data = request.get_json()
        
        # 基本验证
        required_fields = ['age', 'annual_income', 'current_assets', 'monthly_expenses', 'retirement_age']
        for field in required_fields:
            if field not in user_data:
                return jsonify({"success": False, "error": f"缺少字段: {field}"}), 400
        
        # 转换为整数
        age = int(user_data['age'])
        income = int(user_data['annual_income'])
        assets = int(user_data['current_assets'])
        expenses = int(user_data['monthly_expenses'])
        retirement_age = int(user_data['retirement_age'])
        risk_profile = user_data.get('risk_profile', 'moderate')
        
        if retirement_age <= age:
            return jsonify({"success": False, "error": "退休年龄必须大于当前年龄"}), 400
        
        # 简化计算逻辑
        years_to_retire = retirement_age - age
        annual_expenses = expenses * 12
        total_needed = annual_expenses * 25  # 简单估算
        monthly_savings = total_needed // (years_to_retire * 12)
        
        # 资产配置
        if risk_profile == 'conservative':
            allocation = {"股票": 20, "债券": 50, "现金": 30}
            risk_name = "保守型"
        elif risk_profile == 'moderate':
            allocation = {"股票": 50, "债券": 40, "现金": 10}
            risk_name = "稳健型"
        else:
            allocation = {"股票": 70, "债券": 25, "现金": 5}
            risk_name = "进取型"
        
        # 调整年龄因素
        if age > 50:
            allocation["股票"] = max(10, allocation["股票"] - 10)
            allocation["债券"] += 10
        
        result = {
            "user_profile": {
                "age": age,
                "annual_income": income,
                "current_assets": assets,
                "monthly_expenses": expenses,
                "retirement_age": retirement_age,
                "risk_profile": risk_name
            },
            "retirement_analysis": {
                "years_to_retire": years_to_retire,
                "total_needed": total_needed,
                "monthly_savings": monthly_savings
            },
            "portfolio_allocation": allocation,
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify({"success": True, "data": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # 获取环境变量中的端口，如果没有则使用5000
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=False)
