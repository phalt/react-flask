import {context} from 'esbuild'
import {sassPlugin} from 'esbuild-sass-plugin'
import {promises as fs} from 'fs'
import path from 'path'

const validEnvironents = ['development', 'production', 'test']
const env = process.env.NODE_ENV || 'development'
if (!validEnvironents.includes(env)) {
    throw new Error('Invalid Environment')
}

const watch = process.argv.includes('watch')

const define = {
    'process.env.NODE_ENV': JSON.stringify(env),
}

const loader = {
    '.eot': 'file',
    '.woff2': 'file',
    '.woff': 'file',
    '.ttf': 'file',
    '.png': 'file',
    '.svg': 'file',
    '.gif': 'file',
}

const target = ['chrome100', 'firefox100']
const minify = env !== 'development'

const entryPoints = [
    'src/js/beckett_page.tsx',
]

// Crawl the js template dir and add everything that looks like a Page as an entrypoint
const jsTemplateDir = path.join('src', 'js', 'template')
for (const blueprint of await fs.readdir(jsTemplateDir)) {
    for (const endpointFile of await fs.readdir(path.join(jsTemplateDir, blueprint))) {
        const endpointFilePath = path.join(jsTemplateDir, blueprint, endpointFile)
        const res = await fs.stat(endpointFilePath)
        if (!res.isFile()) {
            continue
        }
        if (endpointFile.match(/\.type\.ts$/)) {
            continue
        }
        entryPoints.push(endpointFilePath)
    }
}

// esbuild outputs files with hashed names like `global-ABC.js`, so we need to store a mapping of input -> output for
// admin to use later
const entryPointMap = new Map()
const writeMetafilePlugin = {
    name: 'writeMetafilePlugin',
    setup(build) {
        build.initialOptions.metafile = true

        build.onEnd(async result => {
            console.log('Built...')
            Object.entries(result.metafile.outputs).forEach(([builtFile, output]) => {
                if (output.entryPoint) {
                    entryPointMap.set(output.entryPoint, builtFile.substring('src/static/'.length))
                }
            })
            console.log(entryPointMap)
            await fs.writeFile('src/metafile.json', JSON.stringify(Object.fromEntries(entryPointMap.entries())))
        })
    },
}

console.log("Entrypoint files...")
console.log(entryPoints)

const contexts = [
    context({
        bundle: true,
        define,
        entryNames: '[name]-[hash]',
        entryPoints,
        format: 'esm',
        loader,
        minify,
        outdir: 'src/static/js',
        plugins: [writeMetafilePlugin, sassPlugin()],
        sourcemap: true,
        splitting: true,
        target,
    }),
]

console.log('Erasing static')
await fs.rm('src/static/js', {recursive: true, force: true})

await Promise.all(
    contexts.map(async c => {
        const context = await c
        if (watch) {
            await context.watch()
        } else {
            await context.rebuild()
            await context.dispose()
        }
    }),
)
