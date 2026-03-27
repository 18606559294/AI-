import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import ResumeEditorPage from './ResumeEditorPage';
import { api } from '@ai-resume/shared/api';

// Mock API
vi.mock('@ai-resume/shared/api', () => ({
  api: {
    resume: {
      getResume: vi.fn(),
      createResume: vi.fn(),
      updateResume: vi.fn(),
      aiGenerateResume: vi.fn(),
      deleteResume: vi.fn(),
      getResumes: vi.fn(),
    },
  },
}));

// Type-safe mock helper
const mockGetResume = api.resume.getResume as ReturnType<typeof vi.fn>;
const mockCreateResume = api.resume.createResume as ReturnType<typeof vi.fn>;

describe('ResumeEditorPage Component', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    vi.clearAllMocks();
  });

  const renderWithProviders = (ui: React.ReactNode, initialEntries = ['/resumes/1']) => {
    return render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={initialEntries}>
          <Routes>
            <Route path="/resumes/:id" element={ui} />
            <Route path="/resumes/new" element={ui} />
            <Route path="/" element={<div>Home</div>} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );
  };

  const mockResume = {
    id: 1,
    title: '测试简历',
    content: {
      basic_info: {
        name: '测试用户',
        email: 'test@example.com',
      },
      education: [],
      work_experience: [],
      projects: [],
      skills: [],
    },
  };

  it('渲染编辑器页面', async () => {
    mockGetResume.mockResolvedValue(mockResume as any);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByText('测试简历')).toBeInTheDocument();
    });
  });

  it('渲染标签页导航', async () => {
    mockGetResume.mockResolvedValue(mockResume as any);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByText('基本信息')).toBeInTheDocument();
      expect(screen.getByText('教育经历')).toBeInTheDocument();
      expect(screen.getByText('工作经历')).toBeInTheDocument();
      expect(screen.getByText('项目经历')).toBeInTheDocument();
      expect(screen.getByText('技能特长')).toBeInTheDocument();
    });
  });

  it('切换到预览模式', async () => {
    mockGetResume.mockResolvedValue(mockResume as any);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByText('预览')).toBeInTheDocument();
    });

    screen.getByText('预览').click();

    await waitFor(() => {
      expect(screen.getByText('编辑')).toBeInTheDocument();
    });
  });

  it('创建新简历', async () => {
    mockCreateResume.mockResolvedValue({
      id: 1,
      title: '新简历',
      content: {
        basic_info: {},
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    } as any);

    renderWithProviders(<ResumeEditorPage />, ['/resumes/new']);

    await waitFor(() => {
      expect(screen.getByText('新简历')).toBeInTheDocument();
    });
  });

  it('显示模板选择器（预览模式）', async () => {
    mockGetResume.mockResolvedValue(mockResume as any);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      screen.getByText('预览').click();
    });

    await waitFor(() => {
      expect(screen.getByText('现代模板')).toBeInTheDocument();
      expect(screen.getByText('经典模板')).toBeInTheDocument();
      expect(screen.getByText('简约模板')).toBeInTheDocument();
    });
  });
});
