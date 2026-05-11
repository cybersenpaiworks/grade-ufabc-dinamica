// vite.config.ts
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: '0.0.0.0',
		port: 5173,
		strictPort: true,
		allowedHosts: ['code.cybersenpaiworks.test3'], // Use o domínio exato aqui
		hmr: {
			host: 'code.cybersenpaiworks.test3',
			protocol: 'ws' // Use 'wss' se estiver usando HTTPS no NPM
		}
	}
});