import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface VkContextType {
  isVk: boolean;
  userId: number | null;
  platform: string | null;
}

const VkContext = createContext<VkContextType>({ isVk: false, userId: null, platform: null });

export function VkProvider({ children }: { children: ReactNode }) {
  const [vkInfo, setVkInfo] = useState<VkContextType>({ isVk: false, userId: null, platform: null });

  useEffect(() => {
    // Check if running inside VK Mini App
    const vkBridge = (window as any).vkBridge;
    if (vkBridge) {
      vkBridge.send('VKWebAppInit').then(() => {
        return vkBridge.send('VKWebAppGetUserInfo');
      }).then((data: any) => {
        setVkInfo({ isVk: true, userId: data.id, platform: data.platform || null });
      }).catch(() => {
        setVkInfo({ isVk: false, userId: null, platform: null });
      });
    } else {
      // Not in VK - normal web mode
      setVkInfo({ isVk: false, userId: null, platform: null });
    }
  }, []);

  return (
    <VkContext.Provider value={vkInfo}>
      {children}
    </VkContext.Provider>
  );
}

export function useVk() {
  return useContext(VkContext);
}
