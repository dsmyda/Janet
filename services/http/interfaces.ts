import z from 'zod'
import * as preloadApi from '../../src/core/preload'

export const ZodPreloadPostBody = z.object({
  name: z.string()
    .min(1, { message: "Name must be at least 1 character long"})
    .max(20, { message: "Name must be at most 20 characters long" })
    // Todo, check if name is nothing but characters and numbers
    .refine(
      async (val) => !preloadApi.exists(val),
      (val) => ({ message: `Preload '${val}' already exists`})
    ),
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

export type Filters = z.infer<typeof ZodPreloadPostBody>['filters']

export const ZodQuestionPostBody = z.object({
  question: z.string()
    .min(1, { message: "Question must be at least 1 character long" })
    .max(250, { message: "Question must be at most 100 characters long" }),
    // Todo, check if name is nothing but characters, numbers and punctuation
  preloadName: z.string().optional(),
  gptParams: z.record(z.any()).optional().default({})
})