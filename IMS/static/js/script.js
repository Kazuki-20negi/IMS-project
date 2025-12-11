document.addEventListener('DOMContentLoaded', function () {
    // --- アコーディオンの開閉ロジック ---
    document.querySelectorAll('.accordion-toggle').forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('is-active');
            const content = button.nextElementSibling;
            content.classList.toggle('is-open');
        });
    });

    // --- ブロック追加と削除のイベント処理 ---
    const mainContainer = document.querySelector('main');
    if (!mainContainer) return;

    mainContainer.addEventListener('click', function(e) {
        // --- ブロック追加ボタンがクリックされた場合 ---
        if (e.target.matches('.add-block-btn')) {
            const button = e.target;
            const blockType = button.dataset.type;
            const categoryId = button.dataset.catId;
            addBlockForm(categoryId, blockType);
        }

        // --- ブロック削除ボタンがクリックされた場合 ---
        if (e.target.matches('.delete-form-btn')) {
            const button = e.target;
            const formToDelete = button.closest('.block-form');
            if (formToDelete) {
                const deleteCheckbox = formToDelete.querySelector('input[type="checkbox"][name$="-DELETE"]');
                if (deleteCheckbox) {
                    deleteCheckbox.checked = true;
                }
                formToDelete.style.display = 'none';
            }
        }
    });

    /**
     * 指定されたカテゴリに新しいブロックフォームを追加する関数
     */
    function addBlockForm(categoryId, blockType) {
        const formContainer = document.getElementById(`form-container-cat-${categoryId}`);
        const emptyFormTemplate = document.getElementById(`empty-form-cat-${categoryId}`);
        const form = formContainer.closest('form');
        const totalFormsInput = form.querySelector(`input[name="cat-${categoryId}-TOTAL_FORMS"]`);

        if (!formContainer || !emptyFormTemplate || !totalFormsInput) {
            console.error(`カテゴリID ${categoryId} のフォーム関連要素が見つかりません。`);
            return;
        }

        const currentFormCount = parseInt(totalFormsInput.value);
        const newBlockForm = emptyFormTemplate.firstElementChild.cloneNode(true);

        newBlockForm.dataset.blockType = blockType;

        const formRegex = /__prefix__/g;
        newBlockForm.querySelectorAll('*').forEach(el => {
            ['id', 'name', 'for'].forEach(attr => {
                if (el.hasAttribute(attr)) {
                    el.setAttribute(attr, el.getAttribute(attr).replace(formRegex, currentFormCount));
                }
            });
        });
        
        const blockTypeInput = newBlockForm.querySelector('input[name$="-block_type"]');
        if (blockTypeInput) {
            blockTypeInput.value = blockType;
        }
        
        const orderInput = newBlockForm.querySelector('input[name$="-order"]');
        if (orderInput) {
            orderInput.value = currentFormCount;
        }

        // JavaScriptで強制的に表示を切り替える
        if (blockType === 'text') {
            const imageField = newBlockForm.querySelector('.image-field');
            if (imageField) {
                imageField.style.display = 'none';
            }
        } else if (blockType === 'image') {
            const contentField = newBlockForm.querySelector('.content-field');
            if (contentField) {
                contentField.style.display = 'none';
            }
        }

        formContainer.append(newBlockForm);
        initTextareaAccordion();
        totalFormsInput.value = currentFormCount + 1;
    }

    function initTextareaAccordion() {
        // class="auto-expand-textarea" を持つすべてのtextareaを探す
        document.querySelectorAll('textarea.auto-expand-textarea').forEach(textarea => {
            // 既にラッパーがある場合はスキップ（多重適用防止）
            if (textarea.parentNode.classList.contains('textarea-wrapper')) return;

            // ラッパー要素を作成
            const wrapper = document.createElement('div');
            wrapper.classList.add('textarea-wrapper');
            
            // textareaをラッパーの中に移動
            textarea.parentNode.insertBefore(wrapper, textarea);
            wrapper.appendChild(textarea);

            // トグルボタンを作成
            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'expand-toggle-btn';
            toggleBtn.innerText = '▼ もっと見る';
            
            // ボタンをラッパーに追加（textareaの下）
            wrapper.appendChild(toggleBtn);

            // ボタンクリック時の挙動
            toggleBtn.addEventListener('click', function() {
                if (textarea.classList.contains('collapsed')) {
                    // 展開する
                    textarea.classList.remove('collapsed');
                    textarea.classList.add('expanded');
                    // 内容に合わせて高さを自動調整
                    textarea.style.height = (textarea.scrollHeight + 10) + 'px'; 
                    toggleBtn.innerText = '▲ 閉じる';
                } else {
                    // 閉じる
                    textarea.classList.remove('expanded');
                    textarea.classList.add('collapsed');
                    textarea.style.height = ''; // CSSの高さに戻す
                    toggleBtn.innerText = '▼ もっと見る';
                }
            });

            // 入力時に高さを自動調整（展開時のみ）
            textarea.addEventListener('input', function() {
                if (textarea.classList.contains('expanded')) {
                    this.style.height = 'auto';
                    this.style.height = (this.scrollHeight + 10) + 'px';
                }
            });
        });
    }

    // 初回実行
    initTextareaAccordion();

});