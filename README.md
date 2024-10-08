# brainly.js
Mobile-API for [Brainly](https://play.google.com/store/apps/details?id=co.brainly) platform for students, parents, and teachers to ask and answer homework questions

## Example
```JavaScript
async function main() {
	const { Brainly } = require("./brainly.js")
	const brainly = new Brainly()
	await brainly.login("username", "password")
}

main()
```
