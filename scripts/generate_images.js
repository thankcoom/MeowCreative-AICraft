#!/usr/bin/env node
/**
 * 自動化圖片生成系統
 * 將 Mermaid 圖表轉換為 PNG，並生成所有必要的圖片
 */

const { exec, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const util = require('util');

const execPromise = util.promisify(exec);

// 配置
const CONFIG = {
    mermaidDir: path.join(__dirname, '..', 'mermaid_diagrams'),
    outputDir: path.join(__dirname, '..', 'output', 'session_20251030_115533', 'images'),
    svgGeneratorScript: path.join(__dirname, '..', 'image_generators', 'svg_generator.py'),
    mermaidConfig: {
        theme: 'base',
        themeVariables: {
            primaryColor: '#3B82F6',
            primaryTextColor: '#fff',
            primaryBorderColor: '#2563EB',
            lineColor: '#6B7280',
            secondaryColor: '#10B981',
            tertiaryColor: '#F59E0B'
        }
    }
};

// 圖片生成配置
const IMAGES_TO_GENERATE = [
    // Mermaid 流程圖
    {
        type: 'mermaid',
        input: 'system_architecture.mmd',
        output: 'system-architecture.png',
        description: 'Social Analyzer 系統架構圖'
    },
    {
        type: 'mermaid',
        input: 'detection_modes.mmd',
        output: 'detection-modes.png',
        description: '四種偵測模式流程圖'
    },
    {
        type: 'mermaid',
        input: 'legality_decision_tree.mmd',
        output: 'legality-decision-tree.png',
        description: '使用場景合法性判斷流程'
    },
    {
        type: 'mermaid',
        input: 'scam_investigation_flow.mmd',
        output: 'scam-investigation-flow.png',
        description: '詐騙查證流程時序圖'
    }
];

/**
 * 確保目錄存在
 */
function ensureDirectoryExists(dirPath) {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        console.log(`✓ 已創建目錄: ${dirPath}`);
    }
}

/**
 * 檢查 mmdc 是否已安裝
 */
async function checkMermaidCLI() {
    try {
        await execPromise('npx -y @mermaid-js/mermaid-cli@latest -V');
        console.log('✓ Mermaid CLI 已就緒');
        return true;
    } catch (error) {
        console.log('⚠️  Mermaid CLI 未安裝，將自動安裝...');
        return false;
    }
}

/**
 * 安裝依賴
 */
async function installDependencies() {
    console.log('\n📦 正在安裝必要依賴...\n');

    try {
        // 安裝 Node.js 依賴
        console.log('正在安裝 Node.js 依賴...');
        execSync('npm install', { stdio: 'inherit' });

        // 安裝 Python 依賴
        console.log('\n正在安裝 Python 依賴...');
        execSync('pip3 install -q pillow cairosvg svgwrite', { stdio: 'inherit' });

        console.log('\n✓ 所有依賴已安裝完成\n');
    } catch (error) {
        console.error('❌ 依賴安裝失敗:', error.message);
        throw error;
    }
}

/**
 * 生成 Mermaid 圖表
 */
async function generateMermaidDiagrams() {
    console.log('\n🎨 正在生成 Mermaid 流程圖...\n');

    const mermaidImages = IMAGES_TO_GENERATE.filter(img => img.type === 'mermaid');

    for (const image of mermaidImages) {
        const inputPath = path.join(CONFIG.mermaidDir, image.input);
        const outputPath = path.join(CONFIG.outputDir, image.output);

        try {
            console.log(`  生成: ${image.description}...`);

            // 使用 npx 直接執行 mermaid-cli，避免本地安裝問題
            const command = `npx -y @mermaid-js/mermaid-cli@latest -i "${inputPath}" -o "${outputPath}" -b transparent -w 1200`;

            await execPromise(command);
            console.log(`  ✓ ${image.output} 已生成`);
        } catch (error) {
            console.error(`  ❌ ${image.output} 生成失敗:`, error.message);
            // 繼續生成其他圖片
        }
    }

    console.log('\n✓ Mermaid 流程圖生成完成\n');
}

/**
 * 生成 SVG 圖表
 */
async function generateSVGCharts() {
    console.log('\n📊 正在生成 SVG 圖表...\n');

    try {
        const outputDir = path.join(CONFIG.outputDir, 'svg');
        ensureDirectoryExists(outputDir);

        // 執行 Python SVG 生成器
        const command = `cd "${path.dirname(CONFIG.svgGeneratorScript)}" && python3 svg_generator.py`;

        const { stdout, stderr } = await execPromise(command);

        if (stdout) console.log(stdout);
        if (stderr) console.error(stderr);

        // 移動生成的 SVG 到正確位置
        const generatedDir = path.join(path.dirname(CONFIG.svgGeneratorScript), 'output', 'generated_images');
        if (fs.existsSync(generatedDir)) {
            const files = fs.readdirSync(generatedDir);
            for (const file of files) {
                const src = path.join(generatedDir, file);
                const dest = path.join(CONFIG.outputDir, file);
                fs.copyFileSync(src, dest);
                console.log(`  ✓ ${file} 已複製到輸出目錄`);
            }
        }

        console.log('\n✓ SVG 圖表生成完成\n');
    } catch (error) {
        console.error('❌ SVG 圖表生成失敗:', error.message);
    }
}

/**
 * 生成圖片清單
 */
function generateImageList() {
    console.log('\n📝 正在生成圖片清單...\n');

    const imageList = [];
    const files = fs.readdirSync(CONFIG.outputDir);

    for (const file of files) {
        const ext = path.extname(file).toLowerCase();
        if (['.png', '.svg', '.jpg', '.jpeg'].includes(ext)) {
            const stats = fs.statSync(path.join(CONFIG.outputDir, file));
            imageList.push({
                filename: file,
                size: stats.size,
                created: stats.birthtime,
                path: path.relative(path.join(CONFIG.outputDir, '..'), path.join(CONFIG.outputDir, file))
            });
        }
    }

    const listPath = path.join(CONFIG.outputDir, 'image-list.json');
    fs.writeFileSync(listPath, JSON.stringify(imageList, null, 2));

    console.log(`✓ 已生成圖片清單: ${listPath}`);
    console.log(`  共 ${imageList.length} 個圖片文件\n`);

    return imageList;
}

/**
 * 生成 Markdown 圖片引用
 */
function generateMarkdownReferences(imageList) {
    console.log('📄 生成 Markdown 引用...\n');

    const markdownPath = path.join(CONFIG.outputDir, 'image-references.md');
    let markdown = '# 文章圖片引用\n\n';
    markdown += '將以下圖片引用複製到文章中適當的位置：\n\n';

    // 分類圖片
    const categories = {
        '系統架構': ['system-architecture', 'comparison-chart'],
        '流程圖': ['detection-modes', 'scam-investigation-flow'],
        '法律合規': ['legality-decision-tree', 'legal-compliance-guide'],
        '資料視覺化': ['confidence-score-chart']
    };

    for (const [category, patterns] of Object.entries(categories)) {
        markdown += `## ${category}\n\n`;

        for (const pattern of patterns) {
            const images = imageList.filter(img => img.filename.includes(pattern));
            for (const img of images) {
                markdown += `![${category}](images/${img.filename})\n`;
                markdown += `*${category}示意圖*\n\n`;
            }
        }
    }

    fs.writeFileSync(markdownPath, markdown);
    console.log(`✓ Markdown 引用已生成: ${markdownPath}\n`);
}

/**
 * 主函數
 */
async function main() {
    console.log('╔════════════════════════════════════════════════════════════╗');
    console.log('║         🎨 喵哩文創部落格自動化圖片生成系統 🎨             ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');

    try {
        // 確保輸出目錄存在
        ensureDirectoryExists(CONFIG.outputDir);

        // 檢查並安裝依賴
        const hasMermaidCLI = await checkMermaidCLI();
        if (!hasMermaidCLI) {
            await installDependencies();
        }

        // 生成各類圖片
        await generateMermaidDiagrams();
        await generateSVGCharts();

        // 生成清單和引用
        const imageList = generateImageList();
        generateMarkdownReferences(imageList);

        console.log('╔════════════════════════════════════════════════════════════╗');
        console.log('║                   ✅ 圖片生成完成！                        ║');
        console.log('╚════════════════════════════════════════════════════════════╝\n');

        console.log('📁 圖片輸出目錄:', CONFIG.outputDir);
        console.log('📄 圖片清單:', path.join(CONFIG.outputDir, 'image-list.json'));
        console.log('📝 Markdown 引用:', path.join(CONFIG.outputDir, 'image-references.md'));
        console.log('\n💡 提示: 現在可以將生成的圖片插入到文章中了！\n');

    } catch (error) {
        console.error('\n❌ 圖片生成過程發生錯誤:', error.message);
        process.exit(1);
    }
}

// 執行主函數
if (require.main === module) {
    main();
}

module.exports = { main, generateMermaidDiagrams, generateSVGCharts };
