# 接口自动化测试项目（API Automation Testing）

基于 Python + Pytest + Requests + YAML 的 REST API 自动化测试框架。项目旨在通过自动化手段验证接口的正常业务逻辑、边界值与异常处理，提升回归测试效率。

## 🛠️ 技术栈
- **编程语言**：Python 3
- **测试框架**：Pytest
- **请求库**：Requests
- **数据驱动**：YAML
- **报告生成**：pytest-html

## 📁 项目结构
- `config/`：环境配置（如基础 URL、超时时间）
- `data/`：测试数据（YAML 文件，实现数据与代码分离）
- `tests/`：测试用例（包含正常、边界、异常和业务链路测试）
- `pytest.ini`：测试框架配置

## ✨ 项目亮点
1. **三层断言体系**：从 HTTP 状态码到响应结构，再到业务字段，层层把关。
2. **数据驱动**：使用 YAML 文件管理边界测试数据，新增用例无需修改代码。
3. **异常测试**：验证接口在参数缺失、查询不存在资源时的容错能力。
4. **自动化报告**：集成 pytest-html，生成可视化测试报告。

## 🚀 如何运行
```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试并生成报告
python -m pytest --html=reports/report.html --self-contained-html
