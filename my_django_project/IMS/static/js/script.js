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
     * 指定されたカテゴリに新しいブロックフォームを追加する関数（最終修正版）
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

        // ★★★ ここからが最終手段のコード ★★★
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
        // ★★★ ここまで ★★★

        formContainer.append(newBlockForm);
        totalFormsInput.value = currentFormCount + 1;
    }
});