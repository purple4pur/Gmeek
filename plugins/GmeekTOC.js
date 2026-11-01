function createTOC() {
    var tocElement = document.createElement('div');
    tocElement.className = 'toc';
    var contentContainer = document.getElementById('content');
    
    const headings = contentContainer.querySelectorAll('h1, h2, h3, h4, h5, h6');
    
    if (headings.length === 0) {
        return;  // 如果没有标题元素，则不创建TOC
    }
    
    tocElement.insertAdjacentHTML('afterbegin', '<div class="toc-title">文章目录</div>');
    
    headings.forEach(heading => {
        if (!heading.id) {
            heading.id = heading.textContent.trim().replace(/\s+/g, '-').toLowerCase();
        }
        const link = document.createElement('a');
        link.href = '#' + heading.id;
        link.textContent = heading.textContent;
        link.className = 'toc-link';
        link.style.paddingLeft = `${(parseInt(heading.tagName.charAt(1)) - 1) * 10}px`;
        tocElement.appendChild(link);
    });
    
    const backToTop = document.createElement('button');
    backToTop.type = 'button';
    backToTop.className = 'toc-end';
    backToTop.textContent = 'Top';
    backToTop.addEventListener('click', () => {
        const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.scrollTo({top: 0, behavior: reduce ? 'auto' : 'smooth'});
    });
    tocElement.appendChild(backToTop);
    contentContainer.prepend(tocElement);
}

document.addEventListener("DOMContentLoaded", function() {
    createTOC();
    var css = `
    .toc {
        position:fixed;
        top:130px;
        left:50%;
        transform: translateX(50%) translateX(320px);
        width:200px;
        border: 1px solid var(--color-border-default, #e1e4e8);
        border-radius: 6px;
        padding: 10px;
        overflow-y: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        max-height: 70vh;
    }
    .toc-title{
        font-weight: bold;
        text-align: center;
        border-bottom: 1px solid var(--color-border-default, #ddd);
        padding-bottom: 8px;
    }
    .toc-end{
        width: 100%;
        margin-top: 8px;
        padding: 8px;
        font: inherit;
        font-weight: bold;
        text-align: center;
        cursor: pointer;
        border: 0;
        border-radius: 6px;
        color: inherit;
        background: transparent;
        visibility: hidden;
    }
    .toc-end:hover{background-color: var(--color-action-list-item-default-hover-bg, rgba(0,0,0,0.06));}  
    .toc a {
        display: block;
        color: var(--color-diff-blob-addition-num-text);
        text-decoration: none;
        padding: 5px 0;
        font-size: 14px;
        line-height: 1.5;
        border-bottom: 1px solid var(--color-border-default, #e1e4e8);
    }
    .toc a:last-child {
        border-bottom: none;
    }
    .toc a:hover {
        background-color:var(--color-select-menu-tap-focus-bg);
    }

    @media (max-width: 1249px) 
    {
        .toc{
            position:static;
            top:auto;
            left:auto;
            transform:none;
            padding:10px;
            margin-bottom:20px;
        }
    }`;

    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    const backToTopButton = document.querySelector('.toc-end');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            const scrolled = document.body.scrollTop > 20 || document.documentElement.scrollTop > 20;
            backToTopButton.style.visibility = scrolled ? 'visible' : 'hidden';
        }, {passive: true});
    }

    console.log("\n %c GmeekTOC Plugins https://github.com/Meekdai/Gmeek \n","padding:5px 0;background:#C333D0;color:#fff");
});
