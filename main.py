from aiofauna import *
from uuid import uuid4

class Tiptap(Document):
		id:str = Field(default_factory=lambda: str(uuid4()))
		content:str = Field(default="Hello World")

class Id(Document):
		id:str = Field(default_factory=lambda: str(uuid4()))

app = APIServer()

@app.get("/")
@template()
async def index():
	"""
	<h1 text-red-500 >Editor</h1>
	<div id="{{ id }}"></div>
	<button hx-get="/editor"
		hx-target="#{{ id }}" hx-trigger="click" hx-swap="beforeend">
		Edit
	</button>
	<div id="{{ id }}"></div>
	"""
	return Id()


async def index_endpoint():
	return await index()

@app.get("/editor")
@component
async def tiptap():
	"""
		<div id="{{ id }}"
		hx-get="/documents"
		></div>
	<script type="module">
		import { Editor } from 'https://esm.sh/@tiptap/core'
		import StarterKit from 'https://esm.sh/@tiptap/starter-kit'
		import Image from 'https://esm.sh/@tiptap/extension-image'
		import Link from 'https://esm.sh/@tiptap/extension-link'
		import Placeholder from 'https://esm.sh/@tiptap/extension-placeholder'
		import Underline from 'https://esm.sh/@tiptap/extension-underline'
		import Highlight from 'https://esm.sh/@tiptap/extension-highlight'
		import CodeBlock from 'https://esm.sh/@tiptap/extension-code-block'

		const editor = new Editor({
			element: document.getElementById('{{ id }}'),
			extensions: [
				StarterKit,
				Image,
				Link,
				Placeholder,
				Underline,
				Highlight,
				CodeBlock,
			],
			content: `{{ content }}`,
		})
	</script>

	"""
	return Tiptap()


@app.get("/documents")
@md_component()
async def documents_endpoint():
	"""
	# DATEOAS: Documentation as The Engine of Application State
	
	## Example Application

	### Editor

	We define a TipTap block editor as component docstring.

	```html

	<div id="{{ id }}"></div>
	<script type="module">
		import { Editor } from 'https://esm.sh/@tiptap/core'
		import StarterKit from 'https://esm.sh/@tiptap/starter-kit'
		import Image from 'https://esm.sh/@tiptap/extension-image'
		import Link from 'https://esm.sh/@tiptap/extension-link'
		import Placeholder from 'https://esm.sh/@tiptap/extension-placeholder'
		import Underline from 'https://esm.sh/@tiptap/extension-underline'
		import Highlight from 'https://esm.sh/@tiptap/extension-highlight'
		import CodeBlock from 'https://esm.sh/@tiptap/extension-code-block'

		const editor = new Editor({
			element: document.getElementById('{{ id }}'),
			extensions: [
				StarterKit,
				Image,
				Link,
				Placeholder,
				Underline,
				Highlight,
				CodeBlock,
			],
			content: `{{ content }}`,
		})
	</script>
	
		```

	"""
	return {"id": str(uuid4()), "content": "Hello World"}
