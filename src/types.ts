export type TCookieReq = {
    data: {
        type: 'cookie_request';
        site_url: string;
        user_agent: string;
    };
};

interface ElectronAPI {
    getDomainCookies: (data: any) => Promise<any>;
    openExternal: (data: any) => Promise<any>;
    showItemInFolder: (data: any) => Promise<any>;
}
declare global {
    interface Window {
        electronAPI: ElectronAPI;
    }
}
