import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@ai-resume/shared/api';
import type { ResumeContent, Education, WorkExperience, Project } from '@ai-resume/shared/types';

export default function ResumeEditorPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isNew = id === 'new';

  const [activeTab, setActiveTab] = useState(0);
  const [title, setTitle] = useState('我的简历');
  const [isSaving, setIsSaving] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  // 简历内容
  const [content, setContent] = useState<ResumeContent>({
    basic_info: {
      name: '',
      email: '',
      phone: '',
      location: '',
      title: '',
      summary: '',
      job_intention: '',
      self_introduction: '',
    },
    education: [],
    work_experience: [],
    projects: [],
    skills: [],
  });

  // 获取简历详情
  const { data: resume, isLoading } = useQuery({
    queryKey: ['resume', id],
    queryFn: () => api.resume.getResume(Number(id)),
    enabled: !isNew,
  });

  useEffect(() => {
    if (resume) {
      setTitle(resume.title);
      setContent(resume.content ?? {});
    }
  }, [resume]);

  // 保存 mutation
  const saveMutation = useMutation({
    mutationFn: async (data: { title: string; content: ResumeContent }) => {
      if (isNew) {
        return api.resume.createResume(data);
      }
      return api.resume.updateResume(Number(id), data);
    },
    onSuccess: (data) => {
      setIsSaving(false);
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
      if (isNew) {
        navigate(`/resumes/${data.id}`, { replace: true });
      }
    },
    onError: () => {
      setIsSaving(false);
    },
  });

  // AI 生成 mutation
  const generateMutation = useMutation({
    mutationFn: async () => {
      if (isNew) return;
      return api.resume.aiGenerateResume(Number(id), {
        target_position: content.basic_info?.job_intention || '软件工程师',
      });
    },
    onSuccess: (data) => {
      setIsGenerating(false);
      setContent((data?.content ?? {}) as ResumeContent);
    },
    onError: () => {
      setIsGenerating(false);
    },
  });

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await saveMutation.mutateAsync({ title, content });
    } catch (error) {
      alert(error instanceof Error ? error.message : '保存失败');
    }
  };

  const handleAIGenerate = async () => {
    if (isNew) {
      alert('请先保存简历');
      return;
    }
    if (!content.basic_info?.job_intention) {
      alert('请先填写求职意向');
      setActiveTab(0);
      return;
    }
    setIsGenerating(true);
    try {
      await generateMutation.mutateAsync();
    } catch (error) {
      alert(error instanceof Error ? error.message : 'AI 生成失败');
    }
  };

  const addEducation = () => {
    setContent({
      ...content,
      education: [
        ...(content.education || []),
        { school: '', degree: '', major: '' },
      ],
    });
  };

  const updateEducation = (index: number, field: keyof Education, value: string) => {
    const newEducation = [...(content.education || [])];
    newEducation[index] = { ...newEducation[index], [field]: value };
    setContent({ ...content, education: newEducation });
  };

  const removeEducation = (index: number) => {
    setContent({
      ...content,
      education: content.education?.filter((_, i) => i !== index),
    });
  };

  const addWork = () => {
    setContent({
      ...content,
      work_experience: [
        ...(content.work_experience || []),
        { company: '', position: '', description: '' },
      ],
    });
  };

  const updateWork = (index: number, field: keyof WorkExperience, value: string) => {
    const newWork = [...(content.work_experience || [])];
    newWork[index] = { ...newWork[index], [field]: value };
    setContent({ ...content, work_experience: newWork });
  };

  const removeWork = (index: number) => {
    setContent({
      ...content,
      work_experience: content.work_experience?.filter((_, i) => i !== index),
    });
  };

  const addProject = () => {
    setContent({
      ...content,
      projects: [
        ...(content.projects || []),
        { name: '', description: '', tech_stack: [] },
      ],
    });
  };

  const updateProject = (index: number, field: keyof Project, value: string | string[]) => {
    const newProjects = [...(content.projects || [])];
    newProjects[index] = { ...newProjects[index], [field]: value };
    setContent({ ...content, projects: newProjects });
  };

  const removeProject = (index: number) => {
    setContent({
      ...content,
      projects: content.projects?.filter((_, i) => i !== index),
    });
  };

  const addSkill = () => {
    const skill = prompt('请输入技能名称');
    if (skill) {
      setContent({
        ...content,
        skills: [...(content.skills || []), { name: skill }],
      });
    }
  };

  const removeSkill = (index: number) => {
    setContent({
      ...content,
      skills: content.skills?.filter((_, i) => i !== index),
    });
  };

  const tabs = [
    { label: '基本信息', icon: '👤' },
    { label: '教育经历', icon: '🎓' },
    { label: '工作经历', icon: '💼' },
    { label: '项目经历', icon: '🚀' },
    { label: '技能特长', icon: '⚡' },
  ];

  if (isLoading && !isNew) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* 顶部栏 */}
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <Link to="/" className="text-xl font-bold text-primary-600">
              AI 简历
            </Link>

            <div className="flex items-center gap-2 flex-1 mx-8">
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="text-center font-medium text-lg border-b-2 border-transparent hover:border-gray-300 focus:border-primary-500 focus:outline-none px-2 py-1"
              />
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleAIGenerate}
                disabled={isGenerating || isNew}
                className="btn btn-secondary flex items-center gap-2"
              >
                <span>✨</span>
                {isGenerating ? '生成中...' : 'AI 生成'}
              </button>
              <button
                onClick={handleSave}
                disabled={isSaving}
                className="btn btn-primary flex items-center gap-2"
              >
                {isSaving ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    保存中
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    保存
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 标签页导航 */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-1">
            {tabs.map((tab, index) => (
              <button
                key={index}
                onClick={() => setActiveTab(index)}
                className={`px-6 py-3 font-medium transition-colors ${
                  activeTab === index
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <span className="mr-1">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 内容区域 */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-4xl mx-auto px-4 py-8">
          {activeTab === 0 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold mb-4">基本信息</h2>
              <div className="card p-6 space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">姓名</label>
                    <input
                      type="text"
                      value={content.basic_info?.name ?? ''}
                      onChange={(e) => setContent({
                        ...content,
                        basic_info: { ...content.basic_info!, name: e.target.value }
                      })}
                      className="input"
                      placeholder="请输入姓名"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
                    <input
                      type="email"
                      value={content.basic_info?.email ?? ''}
                      onChange={(e) => setContent({
                        ...content,
                        basic_info: { ...content.basic_info!, email: e.target.value }
                      })}
                      className="input"
                      placeholder="请输入邮箱"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">手机号</label>
                    <input
                      type="tel"
                      value={content.basic_info?.phone ?? ''}
                      onChange={(e) => setContent({
                        ...content,
                        basic_info: { ...content.basic_info!, phone: e.target.value }
                      })}
                      className="input"
                      placeholder="请输入手机号"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">所在城市</label>
                    <input
                      type="text"
                      value={content.basic_info?.location ?? ''}
                      onChange={(e) => setContent({
                        ...content,
                        basic_info: { ...content.basic_info!, location: e.target.value }
                      })}
                      className="input"
                      placeholder="请输入所在城市"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">求职意向</label>
                    <input
                      type="text"
                      value={content.basic_info?.job_intention ?? ''}
                      onChange={(e) => setContent({
                        ...content,
                        basic_info: { ...content.basic_info!, job_intention: e.target.value }
                      })}
                      className="input"
                      placeholder="例如：前端工程师"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">个人简介</label>
                  <textarea
                    value={content.basic_info?.summary ?? ''}
                    onChange={(e) => setContent({
                      ...content,
                      basic_info: { ...content.basic_info!, summary: e.target.value }
                    })}
                    className="input min-h-[120px]"
                    placeholder="请输入个人简介"
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 1 && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">教育经历</h2>
                <button onClick={addEducation} className="btn btn-secondary">
                  + 添加教育经历
                </button>
              </div>
              {content.education?.map((edu, index) => (
                <div key={index} className="card p-6 relative">
                  <button
                    onClick={() => removeEducation(index)}
                    className="absolute top-4 right-4 text-gray-400 hover:text-red-500"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">学校</label>
                      <input
                        type="text"
                        value={edu.school}
                        onChange={(e) => updateEducation(index, 'school', e.target.value)}
                        className="input"
                        placeholder="请输入学校名称"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">学历</label>
                      <input
                        type="text"
                        value={edu.degree}
                        onChange={(e) => updateEducation(index, 'degree', e.target.value)}
                        className="input"
                        placeholder="例如：本科、硕士"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">专业</label>
                      <input
                        type="text"
                        value={edu.major ?? ''}
                        onChange={(e) => updateEducation(index, 'major', e.target.value)}
                        className="input"
                        placeholder="请输入专业"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">毕业时间</label>
                      <input
                        type="month"
                        value={edu.end_date ?? ''}
                        onChange={(e) => updateEducation(index, 'end_date', e.target.value)}
                        className="input"
                      />
                    </div>
                  </div>
                </div>
              ))}
              {(!content.education || content.education.length === 0) && (
                <div className="card p-8 text-center text-gray-500">
                  还没有添加教育经历，点击上方按钮添加
                </div>
              )}
            </div>
          )}

          {activeTab === 2 && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">工作经历</h2>
                <button onClick={addWork} className="btn btn-secondary">
                  + 添加工作经历
                </button>
              </div>
              {content.work_experience?.map((work, index) => (
                <div key={index} className="card p-6 relative">
                  <button
                    onClick={() => removeWork(index)}
                    className="absolute top-4 right-4 text-gray-400 hover:text-red-500"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">公司</label>
                      <input
                        type="text"
                        value={work.company}
                        onChange={(e) => updateWork(index, 'company', e.target.value)}
                        className="input"
                        placeholder="请输入公司名称"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">职位</label>
                      <input
                        type="text"
                        value={work.position}
                        onChange={(e) => updateWork(index, 'position', e.target.value)}
                        className="input"
                        placeholder="请输入职位"
                      />
                    </div>
                  </div>
                  <div className="mt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">工作描述</label>
                    <textarea
                      value={work.description ?? ''}
                      onChange={(e) => updateWork(index, 'description', e.target.value)}
                      className="input min-h-[100px]"
                      placeholder="请描述你的工作内容和成就"
                    />
                  </div>
                </div>
              ))}
              {(!content.work_experience || content.work_experience.length === 0) && (
                <div className="card p-8 text-center text-gray-500">
                  还没有添加工作经历，点击上方按钮添加
                </div>
              )}
            </div>
          )}

          {activeTab === 3 && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">项目经历</h2>
                <button onClick={addProject} className="btn btn-secondary">
                  + 添加项目经历
                </button>
              </div>
              {content.projects?.map((project, index) => (
                <div key={index} className="card p-6 relative">
                  <button
                    onClick={() => removeProject(index)}
                    className="absolute top-4 right-4 text-gray-400 hover:text-red-500"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">项目名称</label>
                      <input
                        type="text"
                        value={project.name}
                        onChange={(e) => updateProject(index, 'name', e.target.value)}
                        className="input"
                        placeholder="请输入项目名称"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">担任角色</label>
                      <input
                        type="text"
                        value={project.role ?? ''}
                        onChange={(e) => updateProject(index, 'role', e.target.value)}
                        className="input"
                        placeholder="例如：前端开发"
                      />
                    </div>
                  </div>
                  <div className="mt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">项目描述</label>
                    <textarea
                      value={project.description ?? ''}
                      onChange={(e) => updateProject(index, 'description', e.target.value)}
                      className="input min-h-[100px]"
                      placeholder="请描述项目内容和你的贡献"
                    />
                  </div>
                </div>
              ))}
              {(!content.projects || content.projects.length === 0) && (
                <div className="card p-8 text-center text-gray-500">
                  还没有添加项目经历，点击上方按钮添加
                </div>
              )}
            </div>
          )}

          {activeTab === 4 && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">技能特长</h2>
                <button onClick={addSkill} className="btn btn-secondary">
                  + 添加技能
                </button>
              </div>
              <div className="card p-6">
                <div className="flex flex-wrap gap-2">
                  {content.skills?.map((skill, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-700 rounded-full"
                    >
                      {skill.name}
                      <button
                        onClick={() => removeSkill(index)}
                        className="hover:text-primary-900"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
                {(!content.skills || content.skills.length === 0) && (
                  <p className="text-gray-500 text-center py-4">
                    还没有添加技能，点击上方按钮添加
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
