import bridge from '@vkontakte/vk-bridge';

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        initData: string;
        colorScheme: 'light' | 'dark';
        ready: () => void;
        expand: () => void;
        enableClosingConfirmation?: () => void;
      };
    };
  }
}

export type PlatformPayload =
  | { provider: 'telegram'; init_data: string }
  | { provider: 'vk'; launch_params: string };

export async function detectPlatform(): Promise<PlatformPayload | null> {
  const telegram = window.Telegram?.WebApp;
  if (telegram?.initData) {
    telegram.ready();
    telegram.expand();
    document.documentElement.dataset.platform = 'telegram';
    return { provider: 'telegram', init_data: telegram.initData };
  }

  const params = new URLSearchParams(window.location.search);
  if (params.has('vk_app_id') && params.has('sign')) {
    await bridge.send('VKWebAppInit');
    document.documentElement.dataset.platform = 'vk';
    return { provider: 'vk', launch_params: params.toString() };
  }
  document.documentElement.dataset.platform = 'web';
  return null;
}
