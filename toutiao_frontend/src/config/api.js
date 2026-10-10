/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // 千问API地址 (baseURL + chat/completions)
  apiEndpoint: 'https://maas.qianwenaiapi.com/compatible-mode/v1/chat/completions',
  
  // API Key (从环境变量读取，见 .env.local)
  apiKey: import.meta.env.VITE_DASHSCOPE_API_KEY,
  
  // 使用的模型
  model: 'qwen3.8-max'
}