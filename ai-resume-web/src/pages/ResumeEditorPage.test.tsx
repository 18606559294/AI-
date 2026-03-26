import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, MemoryRouter, Route, Routes } from 'react-router-dom';
import ResumeEditorPage from '../ResumeEditorPage';
import * as api from '@ai-resume/shared/api';

// Mock API
vi.mock('@ai-resume/shared/api', () => ({
  api: {
    resume: {
      getResume: vi.fn(),
      createResume: vi.fn(),
      updateResume: vi.fn(),
      aiGenerateResume: vi.fn(),
      deleteResume: vi.fn(),
      listResumes: vi.fn(),
    },
  },
}));

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
            <Route path="/" element={<div>Home</div>} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );
  };

  it('渲染编辑器页面', async () => {
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

    vi.mocked(api.resume.getResume).mockResolvedValue(mockResume);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByText('测试简历')).toBeInTheDocument();
      expect(screen.getByDisplayValue('测试用户')).toBeInTheDocument();
    });
  });

  it('渲染标签页导航', async () => {
    const mockResume = {
      id: 1,
      title: '测试简历',
      content: {
        basic_info: {},
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    };

    vi.mocked(api.resume.getResume).mockResolvedValue(mockResume);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByText('基本信息')).toBeInTheDocument();
      expect(screen.getByText('教育经历')).toBeInTheDocument();
      expect(screen.getByText('工作经历')).toBeInTheDocument();
      expect(screen.getByText('项目经历')).toBeInTheDocument();
      expect(screen.getByText('技能特长')).toBeInTheDocument();
    });
  });

  it('切换标签页', async () => {
    const mockResume = {
      id: 1,
      title: '测试简历',
      content: {
        basic_info: {},
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    };

    vi.mocked(api.resume.getResume).mockResolvedValue(mockResume);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByText('基本信息')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('教育经历'));

    await waitFor(() => {
      expect(screen.getByText('添加')).toBeInTheDocument();
    });
  });

  it('输入基本信息', async () => {
    const mockResume = {
      id: 1,
      title: '测试简历',
      content: {
        basic_info: {},
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    };

    vi.mocked(api.resume.getResume).mockResolvedValue(mockResume);
    vi.mocked(api.resume.updateResume).mockResolvedValue({
      id: 1,
      title: '更新后的标题',
      content: {
        basic_info: {
          name: '新名字',
        },
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    });

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByDisplayValue('测试简历')).toBeInTheDocument();
    });

    // 修改标题
    const titleInput = screen.getByDisplayValue('测试简历');
    fireEvent.change(titleInput, { target: { value: '新标题' } });
    expect(titleInput).toHaveValue('新标题');
  });

  it('切换到预览模式', async () => {
    const mockResume = {
      id: 1,
      title: '测试简历',
      content: {
        basic_info: {
          name: '测试用户',
        },
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    };

    vi.mocked(api.resume.getResume).mockResolvedValue(mockResume);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      expect(screen.getByText('预览')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('预览'));

    await waitFor(() => {
      expect(screen.getByText('编辑')).toBeInTheDocument();
    });
  });

  it('创建新简历', async () => {
    vi.mocked(api.resume.createResume).mockResolvedValue({
      id: 1,
      title: '新简历',
      content: {
        basic_info: {},
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    });

    renderWithProviders(<ResumeEditorPage />, ['/resumes/new']);

    await waitFor(() => {
      expect(screen.getByText('新简历')).toBeInTheDocument();
    });

    // 点击保存
    const saveButton = screen.getByText('保存');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(api.resume.createResume).toHaveBeenCalled();
    });
  });

  it('AI 生成按钮在新建简历时禁用', async () => {
    renderWithProviders(<ResumeEditorPage />, ['/resumes/new']);

    await waitFor(() => {
      const aiButton = screen.getByText('AI 生成');
      expect(aiButton).toBeDisabled();
    });
  });

  it('显示模板选择器（预览模式）', async () => {
    const mockResume = {
      id: 1,
      title: '测试简历',
      content: {
        basic_info: {},
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    };

    vi.mocked(api.resume.getResume).mockResolvedValue(mockResume);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      fireEvent.click(screen.getByText('预览'));
    });

    await waitFor(() => {
      expect(screen.getByText('现代模板')).toBeInTheDocument();
      expect(screen.getByText('经典模板')).toBeInTheDocument();
      expect(screen.getByText('简约模板')).toBeInTheDocument();
    });
  });

  it('切换模板', async () => {
    const mockResume = {
      id: 1,
      title: '测试简历',
      content: {
        basic_info: {},
        education: [],
        work_experience: [],
        projects: [],
        skills: [],
      },
    };

    vi.mocked(api.resume.getResume).mockResolvedValue(mockResume);

    renderWithProviders(<ResumeEditorPage />);

    await waitFor(() => {
      fireEvent.click(screen.getByText('预览'));
    });

    await waitFor(() => {
      const templateSelect = screen.getByDisplayValue('modern');
      fireEvent.change(templateSelect, { target: { value: 'classic' } });
    });

    await waitFor(() => {
      expect(screen.getByDisplayValue('classic')).toBeInTheDocument();
    });
  });
});
