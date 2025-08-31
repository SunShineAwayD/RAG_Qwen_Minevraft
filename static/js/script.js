document.addEventListener('DOMContentLoaded', function() {
    const queryInput = document.getElementById('query-input');
    const searchBtn = document.getElementById('search-btn');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const answerElement = document.getElementById('answer');
    const sourcesElement = document.getElementById('sources');
    const exampleBtns = document.querySelectorAll('.example-btn');
    
    // 处理搜索按钮点击
    searchBtn.addEventListener('click', performSearch);
    
    // 处理回车键
    queryInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // 处理示例问题点击
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            queryInput.value = this.textContent;
            performSearch();
        });
    });
    
    function performSearch() {
        const query = queryInput.value.trim();
        
        if (!query) {
            alert('请输入问题');
            return;
        }
        
        // 显示加载动画，隐藏结果
        loading.style.display = 'block';
        resultContainer.style.display = 'none';
        
        // 发送API请求
        fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(data => {
            // 隐藏加载动画，显示结果
            loading.style.display = 'none';
            resultContainer.style.display = 'block';
            
            // 显示回答
            answerElement.textContent = data.answer;
            
            // 显示来源
            sourcesElement.innerHTML = '';
            if (data.sources && data.sources.length > 0) {
                data.sources.forEach((source, index) => {
                    const sourceItem = document.createElement('div');
                    sourceItem.className = 'source-item';
                    sourceItem.innerHTML = `
                        <h3>来源 ${index + 1}</h3>
                        <p><strong>问题:</strong> ${source.question}</p>
                        <p><strong>相似度:</strong> ${(source.score * 100).toFixed(2)}%</p>
                        <p><strong>链接:</strong> <a href="${source.source}" target="_blank">${source.source}</a></p>
                    `;
                    sourcesElement.appendChild(sourceItem);
                });
            } else {
                sourcesElement.innerHTML = '<p>没有找到相关来源</p>';
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            alert('查询出错: ' + error.message);
            console.error('Error:', error);
        });
    }
});