import z from 'zod'
import * as preloadApi from './preload'

export const ZodPreloadPostBody = z.object({
  name: z.string()
    .min(1, { message: "Name must be at least 1 character long"})
    .max(20, { message: "Name must be at most 20 characters long" })
    .refine(async (val) => {
      return preloadApi.exists(val)
    }),
  filters: z.object({
    schemas: z.string().array().optional().default(["public"]),
    includeTables: z.string().array().optional().default(["*"]),
    excludeTables: z.string().array().optional().default([])
  }).optional().default({
    schemas: ["public"],
    includeTables: ["*"],
    excludeTables: []
  })
})

export type Filters = z.infer<typeof ZodPromptPostBody>['filters']

export const ZodAnswerPostBody = z.object({
  question: z.string().min(1, { message: "Question must be at least 1 character long" }).max(100, { message: "Question must be at most 100 characters long" }),
  preloadName: z.string().optional(),
  runQuery: z.boolean().optional().default(true),
  gptParams: z.record(z.any()).optional().default({})
})
