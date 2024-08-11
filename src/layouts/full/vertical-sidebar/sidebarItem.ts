// import {
//     ApertureIcon,
//     CopyIcon,
//     LayoutDashboardIcon, LoginIcon, MoodHappyIcon, TypographyIcon, UserPlusIcon, DatabaseIcon, UploadIcon, CloudDownloadIcon
// } from 'vue-tabler-icons';
import {
    LayoutDashboardIcon,
    DatabaseIcon,
    UploadIcon,
    CloudDownloadIcon
} from 'vue-tabler-icons';

export interface menu {
    header?: string;
    title?: string;
    icon?: any;
    to?: string;
    chip?: string;
    chipColor?: string;
    chipVariant?: string;
    chipIcon?: string;
    children?: menu[];
    disabled?: boolean;
    type?: string;
    subCaption?: string;
}

const sidebarItem: menu[] = [
    { header: '概览' },
    {
        title: '仪表盘',
        icon: LayoutDashboardIcon,
        to: '/'
    },
    { header: '数据管理' },
    {
        title: '上传数据',
        icon: UploadIcon,
        to: '/ui/upload'
    },
    {
        title: '数据库',
        icon: DatabaseIcon,
        to: '/ui/database'
    },
    { header: '版本管理' },
    {
        title: '提交版本',
        icon: CloudDownloadIcon,
        to: '/ui/versions'
    },
    // { header: 'utilities' },
    // {
    //     title: 'Typography',
    //     icon: TypographyIcon,
    //     to: '/ui/typography'
    // },
    // {
    //     title: 'Shadow',
    //     icon: CopyIcon,
    //     to: '/ui/shadow'
    // },
    // { header: 'auth' },
    // {
    //     title: 'Login',
    //     icon: LoginIcon,
    //     to: '/auth/login'
    // },
    // {
    //     title: 'Register',
    //     icon: UserPlusIcon,
    //     to: '/auth/register'
    // },
    // { header: 'Extra' },
    // {
    //     title: 'Icons',
    //     icon: MoodHappyIcon,
    //     to: '/icons'
    // },
    // {
    //     title: 'Sample Page',
    //     icon: ApertureIcon,
    //     to: '/sample-page'
    // },
];

export default sidebarItem;
